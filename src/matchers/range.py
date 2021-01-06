"""Shared range patterns."""

import re
from functools import partial

# pylint: disable=import-error
from traiter.pylib.util import to_positive_float, to_positive_int

from ..pylib.consts import CLOSE, DASH, GROUP_STEP, INT, NUMBER, OPEN, SLASH

TO = ['to']
CONJ = ['or', 'and']
DASH_TO = DASH + TO
DASH_TO_CONJ = DASH_TO + CONJ


def range_(span, fields=''):
    """Build the range parts."""
    data = {}

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


def forget(_):
    """Not a range."""
    return {'_forget': True}


MIN = [
    {'TEXT': {'IN': OPEN}},
    {'TEXT': {'REGEX': NUMBER}},
    {'LOWER': {'IN': DASH_TO_CONJ}},
    {'TEXT': {'IN': CLOSE}},
]

LOW = MIN_VAL = [{'TEXT': {'REGEX': NUMBER}}]

HIGH = DASH_LOW = DASH_MAX = [
    {'LOWER': {'IN': DASH_TO}},
    {'TEXT': {'REGEX': NUMBER}},
]

MAX = HIGH_PARENS = [
    {'TEXT': {'IN': OPEN}},
    {'LOWER': {'IN': DASH_TO_CONJ}},
    {'TEXT': {'REGEX': NUMBER}},
    {'TEXT': {'IN': CLOSE}},
]

OR_LOW = OR_HIGH = OR_MAX = [
    {'TEXT': {'IN': DASH}, 'OP': '?'},
    {'LOWER': 'or'},
    {'TEXT': {'REGEX': NUMBER}},
]

OPEN_HIGH = [
    {'TEXT': {'IN': OPEN}},
    {'LOWER': 'or'},
    {'TEXT': {'REGEX': NUMBER}},
]

CLOSE_MAX = [
    {'TEXT': {'IN': DASH_TO_CONJ}},
    {'TEXT': {'REGEX': NUMBER}},
    {'TEXT': {'IN': CLOSE}},
]

RANGE = {
    GROUP_STEP: [
        {
            'label': 'range',
            'on_match': partial(range_, fields='min low high max'),
            'patterns': [
                MIN + LOW + HIGH + MAX,
                MIN + LOW + OR_HIGH + MAX,
                MIN_VAL + LOW + HIGH + MAX,
                MIN_VAL + OR_LOW + HIGH + MAX,
                MIN_VAL + OR_LOW + OR_HIGH + DASH_MAX,
                MIN_VAL + DASH_LOW + HIGH_PARENS + MAX,
            ],
        },
        {
            'label': 'range',
            'on_match': partial(range_, fields='low high max'),
            'patterns': [
                LOW + HIGH + MAX,
                LOW + OR_HIGH + MAX,
                LOW + HIGH + OR_MAX,
                LOW + OPEN_HIGH + CLOSE_MAX,
            ],
        },
        {
            'label': 'range',
            'on_match': partial(range_, fields='min low high'),
            'patterns': [
                MIN + LOW + HIGH,
                MIN + LOW + OR_HIGH,
                MIN_VAL + OR_LOW + HIGH,
            ],
        },
        {
            'label': 'range',
            'on_match': partial(range_, fields='min low max'),
            'patterns': [
                MIN + LOW + MAX,
                MIN_VAL + OR_LOW + DASH_MAX,
            ],
        },
        {
            'label': 'range',
            'on_match': partial(range_, fields='min low'),
            'patterns': [
                MIN + LOW,
            ],
        },
        {
            'label': 'range',
            'on_match': partial(range_, fields='low high'),
            'patterns': [
                LOW + HIGH,
                LOW + OR_HIGH,
            ],
        },
        {
            'label': 'range',
            'on_match': partial(range_, fields='low max'),
            'patterns': [
                LOW + MAX,
            ],
        },
        {
            'label': 'range',
            'on_match': partial(range_, fields='low'),
            'patterns': [
                LOW,
            ],
        },
        {
            'label': 'fraction',
            'on_match': forget,
            'patterns': [[
                {'TEXT': {'REGEX': INT}},
                {'TEXT': {'IN': SLASH}},
                {'TEXT': {'REGEX': INT}},
            ]],
        },
    ],
}
