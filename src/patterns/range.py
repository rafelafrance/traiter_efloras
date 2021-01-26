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

RANGE = [
    {
        'label': 'range.low',
        'patterns': [[FLOAT_TKN]],
    },
    {
        'label': 'range.min.low',
        'patterns': [
            [
                OPEN_TKN,
                {'LOWER': {'REGEX': f'^{FLOAT_RE}{DASH_RE}{CLOSE_RE}{FLOAT_RE}$'}},
            ],
            [
                OPEN_TKN, FLOAT_TKN,
                {'LOWER': {'REGEX': f'^{CONJ_RE}{CLOSE_RE}{FLOAT_RE}$'}},
            ],
        ],
    },
    {
        'label': 'range.low.high',
        'patterns': [
            [FLOAT_TKN, DASH_TKN, FLOAT_TKN],
            [FLOAT_TKN, CONJ_TKN, FLOAT_TKN],
            [{'LOWER': {'REGEX': f'^{FLOAT_RE}{DASH_RE}{FLOAT_RE}$'}}],
         ],
    },
    {
        'label': 'range.low.max',
        'patterns': [
            [FLOAT_TKN, OPEN_TKN, CONJ_TKN, FLOAT_TKN, CLOSE_TKN],
            [
                {'LOWER': {'REGEX': f'^{FLOAT_RE}{OPEN_RE}{DASH_RE}{FLOAT_RE}$'}},
                CLOSE_TKN,
            ],
            [
                {'LOWER': {'REGEX': f'^{FLOAT_RE}{OPEN_RE}{CONJ_RE}$'}},
                FLOAT_TKN, CLOSE_TKN,
            ],
        ],
    },
    {
        'label': 'range.min.low.high',
        'patterns': [
            [
                OPEN_TKN,
                {'LOWER': {'REGEX': f'^{FLOAT_RE}{DASH_RE}{CLOSE_RE}{FLOAT_RE}$'}},
                DASH_TKN, FLOAT_TKN,
            ],
            [
                FLOAT_TKN, DASH_TKN,
                {'LOWER': {'REGEX': (
                    f'^{FLOAT_RE}{DASH_RE}{OPEN_RE}{DASH_RE}{FLOAT_RE}$')}},
                CLOSE_TKN,
            ],
            [
                OPEN_TKN, FLOAT_TKN,
                {'LOWER': {'REGEX': f'^{CONJ_RE}{CLOSE_RE}{FLOAT_RE}$'}},
                CONJ_TKN, FLOAT_TKN,
            ],
            [OPEN_TKN, FLOAT_TKN, CONJ_TKN, CLOSE_TKN, FLOAT_TKN, CONJ_TKN, FLOAT_TKN],
        ],
    },
    {
        'label': 'range.min.low.max',
        'patterns': [
            [
                OPEN_TKN,
                {'TEXT': {'REGEX': (
                    f'^{FLOAT_RE}{DASH_RE}{CLOSE_RE}{FLOAT_RE}{DASH_RE}'
                    f'{OPEN_RE}{DASH_RE}{FLOAT_RE}$')}},
                CLOSE_TKN,
            ],
        ],
        #         MIN_VAL + OR_LOW + DASH_MAX,
    },
    {
        'label': 'range.low.high.max',
        'patterns': [
            [
                {'TEXT': {'REGEX': (
                    f'^{FLOAT_RE}{DASH_RE}{FLOAT_RE}{DASH_RE}{OPEN_RE}'
                    f'{DASH_RE}{FLOAT_RE}$')}},
                CLOSE_TKN,
            ],
            [
                {'LOWER': {'REGEX': (
                    f'^{FLOAT_RE}{DASH_RE}{FLOAT_RE}{DASH_RE}{OPEN_RE}'
                    f'{DASH_RE}{FLOAT_RE}$')}},
                CLOSE_TKN,
            ],
            [
                FLOAT_TKN, CONJ_TKN,
                {'TEXT': {'REGEX': f'^{FLOAT_RE}{OPEN_RE}{CONJ_RE}$'}},
                FLOAT_TKN, CLOSE_TKN,
            ],
            [FLOAT_TKN, CONJ_TKN, FLOAT_TKN, OPEN_TKN, CONJ_TKN, FLOAT_TKN, CLOSE_TKN],
        ],
        #         LOW + OR_HIGH + MAX,
        #         LOW + HIGH + OR_MAX,
        #         LOW + OPEN_HIGH + CLOSE_MAX,
    },
    {
        'label': 'range.min.low.high.max',
        'patterns': [
            [
                OPEN_TKN,
                {'LOWER': {'REGEX': (
                    fr'^{FLOAT_RE}{DASH_RE}{CLOSE_RE}{FLOAT_RE}{DASH_RE}{FLOAT_RE}'
                    fr'{OPEN_RE}{DASH_RE}{FLOAT_RE}$')}},
                CLOSE_TKN,
            ],
            [
                OPEN_TKN,
                {'LOWER': {'REGEX': f'^{FLOAT_RE}{DASH_RE}{CLOSE_RE}{FLOAT_RE}$'}},
                DASH_TKN,
                {'LOWER': {'REGEX': f'^{FLOAT_RE}{OPEN_RE}{DASH_RE}{FLOAT_RE}$'}},
                CLOSE_TKN,
            ],
        ],
        #         # MIN + LOW + OR_HIGH + MAX,
        #         # MIN_VAL + LOW + HIGH + MAX,
        #         # MIN_VAL + OR_LOW + HIGH + MAX,
        #         # MIN_VAL + OR_LOW + OR_HIGH + DASH_MAX,
        #         # MIN_VAL + DASH_LOW + HIGH_PARENS + MAX,
    },
]
