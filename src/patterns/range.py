"""Shared range patterns."""

import re

import spacy
from traiter.consts import CLOSE, DASH, FLOAT_RE, INT_RE, INT_TOKEN_RE, OPEN, SLASH
from traiter.pipes.entity_data import REJECT_MATCH
from traiter.util import to_positive_float, to_positive_int

TO = ['to']
CONJ = ['or', 'and']
DASH_TO = DASH + TO
DASH_TO_CONJ = DASH_TO + CONJ

MIN = [
    {'TEXT': {'IN': OPEN}},
    {'TEXT': {'REGEX': FLOAT_RE}},
    {'LOWER': {'IN': DASH_TO_CONJ}},
    {'TEXT': {'IN': CLOSE}},
]

LOW = MIN_VAL = [{'TEXT': {'REGEX': FLOAT_RE}}]

HIGH = DASH_LOW = DASH_MAX = [
    {'LOWER': {'IN': DASH_TO}},
    {'TEXT': {'REGEX': FLOAT_RE}},
]

MAX = HIGH_PARENS = [
    {'TEXT': {'IN': OPEN}},
    {'LOWER': {'IN': DASH_TO_CONJ}},
    {'TEXT': {'REGEX': FLOAT_RE}},
    {'TEXT': {'IN': CLOSE}},
]

OR_LOW = OR_HIGH = OR_MAX = [
    {'TEXT': {'IN': DASH}, 'OP': '?'},
    {'LOWER': 'or'},
    {'TEXT': {'REGEX': FLOAT_RE}},
]

OPEN_HIGH = [
    {'TEXT': {'IN': OPEN}},
    {'LOWER': 'or'},
    {'TEXT': {'REGEX': FLOAT_RE}},
]

CLOSE_MAX = [
    {'TEXT': {'IN': DASH_TO_CONJ}},
    {'TEXT': {'REGEX': FLOAT_RE}},
    {'TEXT': {'IN': CLOSE}},
]

RANGE_ACTION = 'range.v1'

RANGE = [
    {
        'label': 'range',
        'id': 'min low high max',
        'on_match': RANGE_ACTION,
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
        'id': 'low high max',
        'on_match': RANGE_ACTION,
        'patterns': [
            LOW + HIGH + MAX,
            LOW + OR_HIGH + MAX,
            LOW + HIGH + OR_MAX,
            LOW + OPEN_HIGH + CLOSE_MAX,
        ],
    },
    {
        'label': 'range',
        'id': 'min low high',
        'on_match': RANGE_ACTION,
        'patterns': [
            MIN + LOW + HIGH,
            MIN + LOW + OR_HIGH,
            MIN_VAL + OR_LOW + HIGH,
        ],
    },
    {
        'label': 'range',
        'id': 'min low max',
        'on_match': RANGE_ACTION,
        'patterns': [
            MIN + LOW + MAX,
            MIN_VAL + OR_LOW + DASH_MAX,
        ],
    },
    {
        'label': 'range',
        'id': 'min low',
        'on_match': RANGE_ACTION,
        'patterns': [
            MIN + LOW,
        ],
    },
    {
        'label': 'range',
        'id': 'low high',
        'on_match': RANGE_ACTION,
        'patterns': [
            LOW + HIGH,
            LOW + OR_HIGH,
        ],
    },
    {
        'label': 'range',
        'id': 'low max',
        'on_match': RANGE_ACTION,
        'patterns': [
            LOW + MAX,
        ],
    },
    {
        'label': 'range',
        'id': 'low',
        'on_match': RANGE_ACTION,
        'patterns': [
            LOW,
        ],
    },
    {
        'label': 'fraction',
        'on_match': REJECT_MATCH,
        'patterns': [[
            {'TEXT': {'REGEX': INT_TOKEN_RE}},
            {'TEXT': {'IN': SLASH}},
            {'TEXT': {'REGEX': INT_TOKEN_RE}},
        ]],
    },
]


@spacy.registry.misc(RANGE_ACTION)
def range_(span):
    """Build the range parts."""
    data = {}

    fields = []  # fields.split()
    values = [t.text for t in span if re.match(FLOAT_RE, t.text)]
    all_ints = all([re.search(INT_RE, v) for v in values])
    data['_all_ints'] = all_ints

    for field, value in zip(fields, values):
        if all_ints:
            data[field] = to_positive_int(value)
        else:
            data[field] = to_positive_float(value)

    return data
