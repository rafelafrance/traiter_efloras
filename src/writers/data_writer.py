"""Write training data to a JSONL file."""

import json

from ..spacy_matchers.consts import TERMS, TRAIT_STEP
from ..spacy_matchers.matcher import MATCHERS
from ..spacy_matchers.pipeline import Pipeline

LABELS = set()

# Convert BILUO tags to BIL tags
BILUO2IOB = {'L': 'I', 'U': 'B'}


def biluo2iob(tag):
    """Convert BILUO tags to BIL tags."""
    char = tag[0]
    char = BILUO2IOB.get(char, char)
    return char + tag[1:]


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
        label = entity.label_
        label = label.split('_')
        if len(label) > 1 and tuple(label[-2:]) in LABELS:
            label = '_'.join(label[-2:])
        else:
            label = label[-1]
        entity_offset = (start, end, label)
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
    _get_labels()
    nlp = Pipeline(training=True).nlp
    for row in rows:
        for sent in row['doc'].sents:
            entities = get_entities(sent) + [(999999, 999999, 'sentinel')]
            doc = nlp(sent.text)
            start, end, label = entities.pop(0)
            tags = []
            count = 0
            for token in doc:
                if token.idx >= end:
                    count = 0
                    start, end, label = entities.pop(0)

                if start <= token.idx < end:
                    iob = 'B' if count == 0 else 'I'
                    tags.append(f'{iob}-{label}')
                    count += 1
                else:
                    tags.append('O')
                    count = 0

            line = json.dumps([sent.text, tags])
            args.iob_file.write(line)
            args.iob_file.write('\n')
