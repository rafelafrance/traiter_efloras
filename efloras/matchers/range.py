"""Shared patterns."""

import re
from functools import partial

# pylint: disable=import-error
from traiter.util import to_positive_int, to_positive_float

from .shared import CLOSE, DASH, INT, NUMBER, OPEN

_DASH_TO = DASH + ['to']
_DASH_TO_CONJ = _DASH_TO + ['or', 'and']


def range_(span, fields=''):
    """Build the range parts."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
        _relabel='range',
    )

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
    'groupers': [
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
                    {'LOWER': 'or'},
                    {'TEXT': {'REGEX': NUMBER}},
                ],
            ]
        },
    ],
}
