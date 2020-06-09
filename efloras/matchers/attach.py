"""Attach traits to a plant part."""

from traiter.util import Step  # pylint: disable=import-error

from .descriptor import DESCRIPTOR_LABELS
from .habit import HABIT_LABELS

PLANT_LABELS = set(DESCRIPTOR_LABELS + HABIT_LABELS)


def attach(span):
    """Attach traits to a plant part."""
    tokens = [t for t in span if t._.label == 'part']
    part = 'plant'
    if tokens and tokens[0]._.label:
        part = tokens[0]._.data['value']

    for token in span:
        label = token._.label
        if token._.step != Step.TRAIT or label == 'part':
            continue

        # Relabel the trait to match the plant part
        if label not in PLANT_LABELS:
            dupe = part == label.split('_')[0]
            token._.label = label if dupe else f'{part}_{label}'
        else:
            token._.label = f'plant_{label}'

    return {'_retokenize': False}


ATTACH = {
    'name': 'attach',
    'matchers': [
        {
            'label': 'attach',
            'on_match': attach,
            'patterns': [
                [
                    {'_': {'label': 'part'}},
                    {'_': {'label': {'NOT_IN': ['part', 'suffix_label']}},
                     'OP': '*'},
                ],
                [
                    {'_': {'label': 'suffix_label'}},
                    {'_': {'label': {'NOT_IN': ['part', 'suffix_label']}},
                     'OP': '+'},
                    {'_': {'label': 'part'}},
                ],
                [
                    {'_': {'label': {'NOT_IN': ['part', 'suffix_label']}},
                     'OP': '+'},
                ],
            ],
        },
    ],
}
