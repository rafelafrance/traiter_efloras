#!/usr/bin/env python3

"""Train a new model for NER and entity linking."""

import argparse
import json
import random
import sys
import textwrap
import warnings
from pathlib import Path

import spacy
from spacy.util import compounding, minibatch
from traiter.pylib.util import now

from src.pylib.consts import LINK_STEP
from src.pylib.pipeline import Pipeline


def main(args):
    """Do it."""
    print('=' * 80)
    print(f'{now()} Started')

    all_data = [json.loads(ln) for ln in args.data.readlines()]
    random.shuffle(all_data)

    split1 = int(len(all_data) * args.splits[0])
    split2 = split1 + int(len(all_data) * args.splits[1])
    train_data = all_data[:split1]
    val_data = all_data[split1:split2]
    test_data = all_data[split2:]

    nlp, optimizer, disable_pipes = setup_model(args, all_data)

    if train_data:
        train(args, nlp, optimizer, disable_pipes, train_data, val_data)

    results = []
    if test_data:
        results = score_data(nlp, test_data, 'Test:')

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True)
        nlp.to_disk(output_dir)
        if test_data and args.results_file:
            with open(output_dir / args.results_file, 'w') as json_file:
                for line in results:
                    json_file.write(f'{line}\n')

    print(f'{now()} Finished')


def setup_model(args, all_data):
    """Create or load the model."""
    spacy.util.fix_random_seed(args.seed)
    if args.old_model_name:
        nlp = spacy.load(args.old_model_name)
        ner = nlp.get_pipe('ner')
        optimizer = nlp.resume_training()
        print(f'Loaded model {args.old_model_name}')
    else:
        nlp = Pipeline(gpu='require', training=True).nlp
        nlp.disable_pipes([LINK_STEP])
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
        optimizer = nlp.begin_training(device=0)

    labels = {e[2] for d in all_data for e in d[1]['entities']}
    for label in labels:
        if label not in ner.labels:
            ner.add_label(label)

    disable_pipes = [p for p in nlp.pipe_names if p != 'ner']

    return nlp, optimizer, disable_pipes


def train(args, nlp, optimizer, disable_pipes, train_data, val_data):
    """Train the model."""
    with nlp.disable_pipes(*disable_pipes) and warnings.catch_warnings():
        warnings.filterwarnings('once', category=UserWarning, module='spacy')
        sizes = compounding(1, args.max_batch_size, 1.1)

        for i in range(1, args.iterations + 1):
            random.shuffle(train_data)
            batches = minibatch(train_data, size=sizes)
            losses = {}
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations,
                           sgd=optimizer, drop=0.35, losses=losses)

            note = f'Epoch {i} validation loss = {losses["ner"]:0.4}:'
            score_data(nlp, val_data, note)


def score_data(nlp, data, note):
    """Score the model."""
    union_count, inter_count = 0, 0
    results = []
    for sent in data:
        doc = nlp(sent[0])
        expected = {(e[0], e[1], e[2]) for e in sent[1]['entities']}
        actually = {(e.start_char, e.end_char, e.label_) for e in doc.ents}
        inter = expected & actually
        union_count += len(expected | actually)
        inter_count += len(inter)
        maxi = len(sent[0])

        result = [{'result': 'ok', 'expect': list(i)} for i in inter]

        expected -= inter
        actually -= inter

        pairs = [(e, a) for e in expected for a in actually
                 if overlaps(e, a)]

        result += [{'result': 'missing', 'expect': x}
                   for x in expected if x not in {p[0] for p in pairs}]

        result += [{'result': 'excess', 'actual': x}
                   for x in actually if x not in {p[1] for p in pairs}]

        for expect, actual in pairs:
            if expect[:2] == actual[:2] and expect[2] != actual[2]:
                label = 'label'
            elif expect[2] == actual[2]:
                label = 'span'
            else:
                label = 'error'
            result.append(
                {'result': label, 'expect': expect, 'actual': actual})

            result = sorted(result, key=lambda r, mx=maxi: (
                min(r.get('actual', [mx])[0], r.get('expect', [mx])[0]),
                -max(r.get('actual', [0, 0])[1], r.get('expect', [0, 0])[1])))

            results.append(json.dumps([sent[0], result]))

    score = inter_count / union_count if union_count else 0.0
    print(f'{now()} {note} score = {score:0.4}')
    return results


def overlaps(expect, actual):
    """Check if the actual value overlaps the expected value."""
    return (expect[0] <= actual[0] < expect[1]
            or expect[0] < actual[1] <= expect[1])


def parse_args():
    """Process command-line arguments."""
    description = """Create models from data from the eFloras website."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--data', '-D', type=argparse.FileType(), required=True,
        help="""Input data file for training, validation, & testing sets.""")

    arg_parser.add_argument(
        '--splits', '-s', nargs=3, type=float, default=[0.6, 0.2, 0.2],
        help="""Split the data using these fractions into training,
            validation, and test data sets. The numbers must add to 1.0.
            The default is: 0.6 0.2 0.2.""")

    arg_parser.add_argument(
        '--old-model-name', '-n', default='',
        help="""Path to a model to update. Defaults to a new model.""")

    arg_parser.add_argument(
        '--new-model-name', '-N',
        help="""Name of the new model.""")

    arg_parser.add_argument(
        '--iterations', '-i', type=int, default=30,
        help="""Number of iterations to train. Default = 30.""")

    arg_parser.add_argument(
        '--seed', '-S', type=int, default=0,
        help="""Random number seed.""")

    arg_parser.add_argument(
        '--max-batch-size', '-b', type=int, default=32,
        help="""Maximum batch size. Default = 32.""")

    arg_parser.add_argument(
        '--output-dir', '-O',
        help="""Output directory.""")

    arg_parser.add_argument(
        '--results-file', '-R',
        help="""The results file name. It will go into the --output-dir.""")

    args = arg_parser.parse_args()

    if sum(args.splits) != 1.0:
        sys.exit('Splits must sum to 1.0.')

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
