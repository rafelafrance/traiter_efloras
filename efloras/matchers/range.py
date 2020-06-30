"""Shared range patterns."""

import re
from functools import partial

# pylint: disable=import-error
from traiter.util import to_positive_float, to_positive_int

from .shared import CLOSE, DASH, INT, NUMBER, OPEN
from ..pylib.util import GROUP_STEP

_TO = ['to']
_CONJ = ['or', 'and']
_DASH_TO = DASH + _TO
_DASH_TO_CONJ = _DASH_TO + _CONJ


def range_(span, fields=''):
    """Build the range parts."""
    data = dict(_relabel='range')

    fields = fields.split()
    values = [t.text for t in span if re.match(NUMBER, t.text)]
    all_ints = all([re.search(INT, v) for v in values])
    data['_all_ints'] = all_ints

    for field, value in zip(fields, values):
        if all_ints:
            data[field] = to_positive_int(value)
        else:
            data[field] = to_positive_float(value)

    return data


RANGE = {
    'name': 'range',
    GROUP_STEP: [
        {
            'label': 'range_mlhx',
            'on_match': partial(range_, fields='min low high max'),
            'patterns': [
                [
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'LOWER': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'IN': CLOSE}},

                    {'TEXT': {'REGEX': NUMBER}},

                    {'LOWER': {'IN': _DASH_TO}},
                    {'TEXT': {'REGEX': NUMBER}},

                    {'TEXT': {'IN': OPEN}},
                    {'LOWER': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': CLOSE}},
                ],
            ]
        },
        {
            'label': 'range_lhx',
            'on_match': partial(range_, fields='low high max'),
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},

                    {'LOWER': {'IN': _DASH_TO}},
                    {'TEXT': {'REGEX': NUMBER}},

                    {'TEXT': {'IN': OPEN}},
                    {'LOWER': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': CLOSE}},
                ],
            ]
        },
        {
            'label': 'range_mlx',
            'on_match': partial(range_, fields='min low max'),
            'patterns': [
                [
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'LOWER': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'IN': CLOSE}},

                    {'TEXT': {'REGEX': NUMBER}},

                    {'TEXT': {'IN': OPEN}},
                    {'LOWER': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': CLOSE}},
                ],
            ]
        },
        {
            'label': 'range_mlh',
            'on_match': partial(range_, fields='min low high'),
            'patterns': [
                [
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'LOWER': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'IN': CLOSE}},

                    {'TEXT': {'REGEX': NUMBER}},

                    {'LOWER': {'IN': _DASH_TO}},
                    {'TEXT': {'REGEX': NUMBER}},
                ],
            ]
        },
        {
            'label': 'range_lx',
            'on_match': partial(range_, fields='low max'),
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},

                    {'TEXT': {'IN': OPEN}},
                    {'LOWER': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': CLOSE}},
                ],
            ]
        },
        {
            'label': 'range_lh',
            'on_match': partial(range_, fields='low high'),
            'patterns': [
                [
                    {'LOWER': {'IN': _TO}, 'OP': '?'},
                    {'TEXT': {'REGEX': NUMBER}},

                    {'LOWER': {'IN': _DASH_TO}},
                    {'TEXT': {'REGEX': NUMBER}},
                ],
            ]
        },
        {
            'label': 'range_ml',
            'on_match': partial(range_, fields='min low'),
            'patterns': [
                [
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'LOWER': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'IN': CLOSE}},

                    {'TEXT': {'REGEX': NUMBER}},
                ],
            ]
        },
        {
            'label': 'range_l',
            'on_match': partial(range_, fields='low'),
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},
                ],
            ]
        },
        {
            'label': 'range_lh_or',
            'on_match': partial(range_, fields='low high'),
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'LOWER': 'or'},
                    {'TEXT': {'REGEX': NUMBER}},
                ],
            ]
        },
        {
            'label': 'range_lhx_or',
            'on_match': partial(range_, fields='low high max'),
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'LOWER': 'or'},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': CLOSE}},
                ],
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': OPEN}},
                    {'LOWER': 'or'},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': CLOSE}},
                ],
            ]
        },
        {
            'label': 'range_mlh_or',
            'on_match': partial(range_, fields='min low high'),
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}},
                    {'LOWER': 'or'},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}},
                    {'TEXT': {'REGEX': NUMBER}},
                ],
                [
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'IN': CLOSE}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': _DASH_TO_CONJ}, 'OP': '+'},
                    {'TEXT': {'REGEX': NUMBER}},
                ],
            ]
        },
        {
            'label': 'range_lhm_or',
            'on_match': partial(range_, fields='low high max'),
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}},
                    {'LOWER': 'or'},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': CLOSE}},
                ],
            ]
        },
        {
            'label': 'range_lhmx_or',
            'on_match': partial(range_, fields='min low high max'),
            'patterns': [
                [
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}},
                    {'LOWER': 'or'},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}},
                    {'LOWER': 'or'},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}},
                    {'TEXT': {'REGEX': NUMBER}},
                ],
                [
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'IN': CLOSE}},
                    {'LOWER': 'or', 'OP': '?'},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'LOWER': 'or', 'OP': '?'},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': {'IN': _DASH_TO_CONJ}},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'TEXT': {'IN': CLOSE}},
                ],
            ]
        },
    ],
}
