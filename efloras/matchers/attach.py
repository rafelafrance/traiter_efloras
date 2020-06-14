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

    subpart = ''

    for token in span:
        label = token._.label

        if label == 'subpart':
            subpart = f'_{label}'

        elif token._.step != Step.TRAIT or label == 'part':
            pass

        # Relabel the trait to match the plant part
        elif label not in PLANT_LABELS:
            dupe = part == label.split('_')[0]
            token._.label = label if dupe else f'{part}{subpart}_{label}'
        else:
            token._.label = f'plant_{label}'

    return {'_retokenize': False}


def attach_suffix(span):
    """Attach traits to a plant part that is using a suffix notation."""
    for token in span:
        label = token._.label
        print(label, token.text)

    return {'_retokenize': False}


_STOP_PREFIX = ['part', 'suffix_label']
_STOP_SUFFIX = _STOP_PREFIX + ['subpart']

ATTACH = {
    'name': 'attach',
    'matchers': [
        {
            'label': 'attach',
            'on_match': attach,
            'patterns': [
                [
                    {'_': {'label': 'part'}},
                    {'_': {'label': {'NOT_IN': _STOP_PREFIX}}, 'OP': '*'},
                ],
                [{'_': {'label': {'NOT_IN': _STOP_PREFIX}}, 'OP': '+'}],
            ],
        },
        {
            'label': 'attach_suffix',
            'on_match': attach,
            'patterns': [
                [
                    {'_': {'label': 'suffix_label'}},
                    {'_': {'label': {'NOT_IN': _STOP_SUFFIX}}, 'OP': '+'},
                    {'_': {'label': 'subpart'}},
                ],
            ],
        },
    ],
}
