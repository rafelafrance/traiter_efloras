"""Shared range patterns."""

from traiter.const import CLOSE as CLOSE_, DASH as DASH_, FLOAT_RE, OPEN as OPEN_

TO_ = ['to']
CONJ_ = ['or', 'and']

NUM = {'TEXT': {'REGEX': f'^{FLOAT_RE}$'}}
OPEN = {'TEXT': {'IN': OPEN_}}
CLOSE = {'TEXT': {'IN': CLOSE_}}
CONJ = {'LOWER': {'IN': CONJ_}}
DASH = {'TEXT': {'IN': DASH_}}
TO = {'LOWER': {'IN': DASH_ + TO_}}
OR = {'LOWER': {'IN': DASH_ + TO_ + CONJ_}}

RANGE = [
    {
        'label': 'range.low',
        'patterns': [[NUM]],
    },
    {
        'label': 'range.min.low',
        'patterns': [
            [OPEN, NUM, OR, CLOSE, NUM],
        ],
    },
    {
        'label': 'range.low.high',
        'patterns': [
            [NUM, CONJ, NUM],
            [NUM, DASH, DASH, NUM],
            [NUM, DASH, NUM, DASH, NUM],
            [NUM, DASH, NUM],
        ],
    },
    {
        'label': 'range.low.max',
        'patterns': [
            [NUM, OPEN, CONJ, NUM, CLOSE],
            [NUM, OPEN, DASH, NUM, CLOSE],
        ],
    },
    {
        'label': 'range.min.low.high',
        'patterns': [
            [NUM, DASH, NUM, DASH, OPEN, DASH, NUM, CLOSE],
            [NUM, OPEN, CONJ, NUM, TO, NUM, CLOSE],
            [OPEN, NUM, CONJ, CLOSE, NUM, CONJ, NUM],
            [OPEN, NUM, DASH, CLOSE, NUM, DASH, NUM],
            [OPEN, NUM, OR, CLOSE, NUM, DASH, CONJ, NUM],
        ],
    },
    {
        'label': 'range.min.low.max',
        'patterns': [
            [OPEN, NUM, DASH, CLOSE, NUM, DASH, OPEN, DASH, NUM, CLOSE],
            [NUM, DASH, CONJ, NUM, TO, NUM],
        ],
    },
    {
        'label': 'range.low.high.max',
        'patterns': [
            [NUM, CONJ, NUM, OPEN, CONJ, NUM, CLOSE],
            [NUM, DASH, NUM, CONJ, NUM],
            [NUM, DASH, NUM, DASH, OPEN, DASH, NUM, CLOSE],
            [NUM, DASH, NUM, OPEN, DASH, NUM, CLOSE],
            [NUM, DASH, CONJ, NUM, OPEN, OR, NUM, CLOSE],
            [NUM, TO, NUM, CONJ, NUM],
            [NUM, OPEN, CONJ, NUM, OR, NUM, CLOSE],
        ],
    },
    {
        'label': 'range.min.low.high.max',
        'patterns': [
            [NUM, CONJ, NUM, DASH, NUM, OPEN, OR, NUM, CLOSE],
            [OPEN, NUM, CONJ, CLOSE, NUM, DASH, CONJ, NUM, OPEN, CONJ, NUM, CLOSE],
            [OPEN, NUM, DASH, CLOSE, NUM, DASH, NUM, OPEN, DASH, NUM, CLOSE],
            [OPEN, NUM, DASH, CLOSE, NUM, DASH,NUM, OPEN, DASH, NUM, CLOSE],
            [OPEN, NUM, OR, CLOSE, NUM, DASH, CONJ, NUM, OPEN, OR, NUM, CLOSE],
            [NUM, NUM, TO, CONJ, NUM, OPEN, OR, NUM, CLOSE],
            [NUM, DASH, CONJ, NUM, TO, NUM, OPEN, OR, NUM, CLOSE],
            [NUM, DASH, CONJ, NUM, DASH, CONJ, NUM, TO, NUM],
            [NUM, TO, NUM, OPEN, OR, NUM, CLOSE, OPEN, OR, NUM, CLOSE],
        ],
    },
]
