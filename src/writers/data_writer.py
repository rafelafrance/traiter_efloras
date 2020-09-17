"""Write training data to a JSONL file."""

import json

from ..matchers.matcher import MATCHERS
from ..pylib.util import TERMS, TRAIT_STEP

LABELS = set()


def _get_labels():
    """Get the suffix lengths of the traits."""
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


def _training_data_writer(rows):
    """Output the data."""
    _get_labels()
    lines = []
    for row in rows:
        # Initialize sentences
        sents = [{'start': s.start_char, 'end': s.end_char}
                 for s in row['doc'].sents]

        # Initialize traits
        traits = []
        for trait in row['traits']:
            traits.append({
                'start': trait['start'],
                'end': trait['end'],
                'label': trait['trait'],
            })
        traits = sorted(
            traits, key=lambda t: (t['start'], t['end'], t['label']))

        # Attach traits to a sentence
        for sent in sents:
            sent['traits'] = [t for t in traits
                              if t['start'] >= sent['start']
                              and t['end'] <= sent['end']]

        # Write the data
        for sent in sents:
            text = row['text'][sent['start']:sent['end']]
            traits = []
            for trait in sent['traits']:
                start = trait['start'] - sent['start']
                end = trait['end'] - sent['start']
                label = trait['label']
                label = label.split('_')
                if len(label) > 1 and tuple(label[-2:]) in LABELS:
                    label = '_'.join(label[-2:])
                traits.append((start, end, label))
            lines.append(json.dumps([text, {'entities': traits}]))
    return lines


def ner_writer(args, rows):
    """Output named entity recognition training data."""
    for row in _training_data_writer(rows):
        args.ner_file.write(row[0], row[1])
        args.ner_file.write('\n')
