"""Patterns for attaching traits to plant parts."""

from traiter.util import Step  # pylint: disable=import-error
from ..matchers.shared import DOT


def attach_final_suffix(span):
    """Attach traits to a plant part."""
    part = ''
    for token in list(span)[::-1]:
        if token._.label == 'part':
            part = token._.data['part']
        elif token._.step == Step.TRAIT:
            token._.label = f'{part}_{token._.label}'
        token._.aux['attached'] = True
    return {'_retokenize': False}


ATTACH = {
    'name': 'attach',
    'matchers': [
        {
            'label': 'attach',
            'on_match': attach_final_suffix,
            'patterns': [
                [
                    {'LOWER': 'and'},
                    {'_': {'step': Step.TRAIT}},
                    {'_': {'label': 'part'}},
                    {'TEXT': {'IN': DOT}}
                ],
            ],
        },
    ],
}
