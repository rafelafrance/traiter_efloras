"""Patterns for attaching traits to plant parts."""

from ..matchers.shared import DOT
from ..pylib.attach_fsm import TRAIT_STEP


def attach_final_suffix(span):
    """Attach traits to a plant part."""
    part = ''
    for token in list(span)[::-1]:
        if token._.label == 'part':
            part = token._.data['part']
        elif token._.step == TRAIT_STEP:
            token._.label = f'{part}_{token._.label}'
        token._.aux['attached'] = True
    return {'_retokenize': False}


def attach_retokenize(span):
    """Attach traits to a subpart."""
    label, subpart, data = '', '', {}
    for token in list(span):
        if token._.label == 'subpart':
            subpart = token._.data['subpart']
        elif token._.step == TRAIT_STEP:
            data = token._.data
            label = token._.label
        token._.aux['subpart_attached'] = True
    data['_relabel'] = f'{subpart}_{label}'
    return data


ATTACH = {
    'name': 'attach',
    'matchers': [
        {
            'label': 'attach',
            'on_match': attach_final_suffix,
            'patterns': [
                [
                    {'LOWER': 'and'},
                    {'_': {'step': TRAIT_STEP}},
                    {'_': {'label': 'part'}},
                    {'TEXT': {'IN': DOT}}
                ],
            ],
        },
        {
            'label': 'attach_retokenize',
            'on_match': attach_retokenize,
            'patterns': [
                [
                    {'LOWER': {'IN': ['with', 'having']}},
                    {'LOWER': 'a', 'OP': '?'},
                    {'_': {'label': 'subpart'}},
                    {'_': {'step': TRAIT_STEP}},
                ],
            ],
        },
    ],
}
