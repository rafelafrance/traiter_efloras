"""Shared range patterns."""
from traiter.consts import CLOSE, CLOSE_RE, DASH, DASH_RE, FLOAT_RE, OPEN, OPEN_RE

TO = ['to']
CONJ = ['or', 'and']
DASH_TO = DASH + TO
DASH_TO_CONJ = DASH_TO + CONJ

CONJ_RE = r'\s*(or|and)\s*'

FLOAT_TKN = {'TEXT': {'REGEX': f'^{FLOAT_RE}$'}}
OPEN_TKN = {'TEXT': {'IN': OPEN}}
CLOSE_TKN = {'TEXT': {'IN': CLOSE}}
DASH_TKN = {'TEXT': {'IN': DASH}}
CONJ_TKN = {'LOWER': {'IN': CONJ}}

CONJ_CLOSE_FLOAT = {'LOWER': {'REGEX': f'^{CONJ_RE}{CLOSE_RE}{FLOAT_RE}$'}}
FLOAT_OPEN_CONJ = {'LOWER': {'REGEX': f'^{FLOAT_RE}{OPEN_RE}{CONJ_RE}$'}}
FLOAT_OPEN_DASH_FLOAT = {
    'LOWER': {'REGEX': f'^{FLOAT_RE}{OPEN_RE}{DASH_RE}{FLOAT_RE}$'}}
FLOAT_CONJ_CLOSE_FLOAT = {'LOWER': {'REGEX': (
    f'^{FLOAT_RE}{CONJ_RE}{CLOSE_RE}{FLOAT_RE}$')}}
FLOAT_CONJ_CLOSE_FLOAT_DASH = {'LOWER': {'REGEX': (
    f'^{FLOAT_RE}{CONJ_RE}{CLOSE_RE}{FLOAT_RE}{DASH_RE}$')}}
FLOAT_DASH_FLOAT = {'LOWER': {'REGEX': f'^{FLOAT_RE}{DASH_RE}{FLOAT_RE}$'}}
FLOAT_DASH_CLOSE_FLOAT = {
    'LOWER': {'REGEX': f'^{FLOAT_RE}{DASH_RE}{CLOSE_RE}{FLOAT_RE}$'}}
FLOAT_DASH_OPEN_DASH_FLOAT = {
    'LOWER': {'REGEX': f'^{FLOAT_RE}{DASH_RE}{OPEN_RE}{DASH_RE}{FLOAT_RE}$'}}
FLOAT_DASH_FLOAT_OPEN_CONJ = {'LOWER': {'REGEX': (
    f'^{FLOAT_RE}{DASH_RE}{FLOAT_RE}{OPEN_RE}{CONJ_RE}$')}}
FLOAT_DASH_FLOAT_OPEN_DASH_FLOAT = {'LOWER': {'REGEX': (
    f'^{FLOAT_RE}{DASH_RE}{FLOAT_RE}{OPEN_RE}{DASH_RE}{FLOAT_RE}$')}}
FLOAT_DASH_FLOAT_DASH_OPEN_DASH_FLOAT = {'TEXT': {'REGEX': (
    f'^{FLOAT_RE}{DASH_RE}{FLOAT_RE}{DASH_RE}{OPEN_RE}{DASH_RE}{FLOAT_RE}$')}}
FLOAT_DASH_CLOSE_FLOAT_DASH_OPEN_DASH_FLOAT = {'TEXT': {'REGEX': (
    f'^{FLOAT_RE}{DASH_RE}{CLOSE_RE}{FLOAT_RE}{DASH_RE}{OPEN_RE}{DASH_RE}{FLOAT_RE}$')}}
FLOAT_DASH_CLOSE_FLOAT_DASH_FLOAT_OPEN_DASH_FLOAT = {'LOWER': {'REGEX': (
    f'^{FLOAT_RE}{DASH_RE}{CLOSE_RE}{FLOAT_RE}{DASH_RE}{FLOAT_RE}'
    f'{OPEN_RE}{DASH_RE}{FLOAT_RE}$')}}

RANGE = [
    {
        'label': 'range.low',
        'patterns': [[FLOAT_TKN]],
    },
    {
        'label': 'range.min.low',
        'patterns': [
            [OPEN_TKN, FLOAT_DASH_CLOSE_FLOAT],
            [OPEN_TKN, FLOAT_TKN, CONJ_CLOSE_FLOAT],
        ],
    },
    {
        'label': 'range.low.high',
        'patterns': [
            [FLOAT_TKN, DASH_TKN, FLOAT_TKN],
            [FLOAT_TKN, CONJ_TKN, FLOAT_TKN],
            [FLOAT_DASH_FLOAT],
            [FLOAT_TKN, DASH_TKN, FLOAT_DASH_FLOAT],
         ],
    },
    {
        'label': 'range.low.max',
        'patterns': [
            [FLOAT_TKN, OPEN_TKN, CONJ_TKN, FLOAT_TKN, CLOSE_TKN],
            [FLOAT_OPEN_DASH_FLOAT, CLOSE_TKN],
            [FLOAT_OPEN_CONJ, FLOAT_TKN, CLOSE_TKN],
        ],
    },
    {
        'label': 'range.min.low.high',
        'patterns': [
            [OPEN_TKN, FLOAT_DASH_CLOSE_FLOAT, DASH_TKN, FLOAT_TKN],
            [OPEN_TKN, FLOAT_TKN, CONJ_CLOSE_FLOAT, CONJ_TKN, FLOAT_TKN],
            [OPEN_TKN, FLOAT_TKN, CONJ_TKN, CLOSE_TKN, FLOAT_TKN, CONJ_TKN, FLOAT_TKN],
            [FLOAT_TKN, DASH_TKN, FLOAT_DASH_OPEN_DASH_FLOAT, CLOSE_TKN],
        ],
    },
    {
        'label': 'range.min.low.max',
        'patterns': [
            [OPEN_TKN, FLOAT_DASH_CLOSE_FLOAT_DASH_OPEN_DASH_FLOAT, CLOSE_TKN],
        ],
        #         MIN_VAL + OR_LOW + DASH_MAX,
    },
    {
        'label': 'range.low.high.max',
        'patterns': [
            [FLOAT_TKN, CONJ_TKN, FLOAT_OPEN_CONJ, FLOAT_TKN, CLOSE_TKN],
            [FLOAT_TKN, CONJ_TKN, FLOAT_TKN, OPEN_TKN, CONJ_TKN, FLOAT_TKN, CLOSE_TKN],
            [FLOAT_DASH_FLOAT, CONJ_TKN, FLOAT_TKN],
            [FLOAT_DASH_FLOAT_DASH_OPEN_DASH_FLOAT, CLOSE_TKN],
            [FLOAT_DASH_FLOAT_OPEN_DASH_FLOAT, CLOSE_TKN],
        ],
        #         LOW + OR_HIGH + MAX,        #         LOW + HIGH + OR_MAX,
        #         LOW + OPEN_HIGH + CLOSE_MAX,
    },
    {
        'label': 'range.min.low.high.max',
        'patterns': [
            [FLOAT_TKN, CONJ_TKN, FLOAT_DASH_FLOAT_OPEN_CONJ, FLOAT_TKN, CLOSE_TKN],
            [OPEN_TKN, FLOAT_DASH_CLOSE_FLOAT_DASH_FLOAT_OPEN_DASH_FLOAT, CLOSE_TKN],
            [
                OPEN_TKN, FLOAT_DASH_CLOSE_FLOAT, DASH_TKN,
                FLOAT_OPEN_DASH_FLOAT, CLOSE_TKN,
            ],
            [
                OPEN_TKN, FLOAT_CONJ_CLOSE_FLOAT_DASH,
                CONJ_TKN, FLOAT_OPEN_CONJ, FLOAT_TKN, CLOSE_TKN,
            ],
            [
                OPEN_TKN, FLOAT_CONJ_CLOSE_FLOAT,
                DASH_TKN, CONJ_TKN, FLOAT_OPEN_CONJ, FLOAT_TKN, CLOSE_TKN,
            ],
        ],
        #         # MIN + LOW + OR_HIGH + MAX,
        #         # MIN_VAL + LOW + HIGH + MAX,
        #         # MIN_VAL + OR_LOW + HIGH + MAX,
        #         # MIN_VAL + OR_LOW + OR_HIGH + DASH_MAX,
        #         # MIN_VAL + DASH_LOW + HIGH_PARENS + MAX,
    },
]
