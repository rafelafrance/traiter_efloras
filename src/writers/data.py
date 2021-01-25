"""Write training data to a JSONL file."""

import json

from ..pylib.consts import TERMS, TRAIT_STEP
from ..patterns.matcher import MATCHERS
from src.pylib.pipeline import Pipeline

LABELS = set()


def _get_labels():
    """Get the suffix lengths of the traits."""
    if LABELS:
        return
    for matcher in MATCHERS:
        for step, step_patterns in matcher.items():
            if step == TRAIT_STEP:
                for pattern_group in step_patterns:
                    label = pattern_group['label'].split('_')
                    if label[0]:
                        LABELS.add(tuple(label))
    for term in TERMS:
        if term['category'] in {'descriptor', 'literal'}:
            label = term['label'].split('_')
            LABELS.add(tuple(label))


def get_entities(sent):
    """Convert traits in a sentence to entity offsets."""
    entities = []
    for entity in sent.ents:
        start = entity.start_char - sent.start_char
        end = entity.end_char - sent.start_char
        entity_offset = (start, end, entity.label_)
        entities.append(entity_offset)
    return entities


def ner_writer(args, rows):
    """Output named entity recognition training data."""
    _get_labels()
    for row in rows:
        for sent in row['doc'].sents:
            entities = get_entities(sent)
            line = json.dumps([sent.text, {'entities': entities}])
            args.ner_file.write(line)
            args.ner_file.write('\n')


def iob_writer(args, rows):
    """Output named entity recognition training data in BIO format."""
    out_file = args.iob_file
    iob_biluo_writer(out_file, rows, lambda *_: None)


def biluo_writer(args, rows):
    """Output named entity recognition training data in BIO format."""
    out_file = args.biluo_file
    iob_biluo_writer(out_file, rows, update_prev_tag)


def iob_biluo_writer(out_file, rows, updater):
    """Logic common to both the IOB and BILUO writers."""
    _get_labels()
    nlp = Pipeline(training=True).nlp
    for row in rows:
        for sent in row['doc'].sents:
            entities = get_entities(sent) + [(9_999_999, 9_999_999, '')]
            doc = nlp(sent.text)
            start, end, label = entities.pop(0)
            tags = []
            inside = False
            for token in doc:
                if token.idx >= end:
                    inside = False
                    start, end, label = entities.pop(0)

                if start <= token.idx < end:
                    prefix = 'I' if inside else 'B'
                    if prefix == 'B':
                        updater(tags)
                    tags.append(f'{prefix}-{label}')
                    inside = True
                else:
                    updater(tags)
                    tags.append('O')
                    inside = False

            updater(tags)
            line = json.dumps([sent.text, tags])
            out_file.write(line)
            out_file.write('\n')


def update_prev_tag(tags):
    """Update the previous tags for BILUO tagging scheme."""
    prev = tags[-1] if tags else ''
    if prev.startswith('I'):
        tags[-1] = 'L' + prev[1:]
    if prev.startswith('B'):
        tags[-1] = 'U' + prev[1:]
