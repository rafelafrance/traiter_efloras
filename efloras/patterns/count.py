"""Common count snippets."""

import re

import spacy
from traiter.const import CLOSE, CROSS, DASH, FLOAT_RE, INT_TOKEN_RE, OPEN, SLASH
from traiter.pipe_util import REJECT_MATCH, RejectMatch
from traiter.util import to_positive_int

from ..pylib.const import IS_RANGE, REPLACE

NOT_COUNT_WORDS = CROSS + SLASH + """ average side times days weeks by """.split()

NOT_COUNT_ENTS = """ imperial_length metric_mass imperial_mass """.split()

COUNT = [
    {
        'label': 'count',
        'after_match': {'func': 'count.v1'},
        'patterns': [
            [
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'per_count', 'OP': '?'},
                {'ENT_TYPE': 'count_suffix', 'OP': '?'},
            ],
            [
                {'ENT_TYPE': IS_RANGE},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': 'per_count', 'OP': '?'},
            ],
            [
                {'ENT_TYPE': 'per_count'},
                {'POS': {'IN': ['ADP']}, 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'count_suffix', 'OP': '?'},
            ],
            [
                {'TEXT': {'IN': OPEN}},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'count_suffix', 'OP': '?'},
                {'TEXT': {'IN': CLOSE}},
                {'ENT_TYPE': 'per_count'},
            ],
        ],
    },
    {
        'label': 'count_word',
        'after_match': {'func': 'count_word.v1'},
        'patterns': [
            [
                {'ENT_TYPE': 'count_word'},
            ],
        ],
    },
    {
        'label': '_not_a_count',
        'after_match': {'func': REJECT_MATCH},
        'patterns': [
            [
                {'ENT_TYPE': IS_RANGE},
                {'LOWER': {'IN': NOT_COUNT_WORDS}},
                {'ENT_TYPE': IS_RANGE, 'OP': '?'},
            ],
            [
                {'ENT_TYPE': IS_RANGE},
                {'LOWER': {'IN': NOT_COUNT_WORDS}},
                {'ENT_TYPE': IS_RANGE, 'OP': '?'},
                {'ENT_TYPE': {'IN': NOT_COUNT_ENTS}, 'OP': '?'},
            ],
            [
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': {'IN': NOT_COUNT_ENTS}},
            ],
        ],
    },
]


@spacy.registry.misc(COUNT[0]['after_match']['func'])
def count(ent):
    """Enrich the match with data."""
    print('count', ent)
    range_ = range_values(ent)

    if per_count_ := [e for e in ent.ents if e.label_ == 'per_count']:
        per_count_ = per_count_[0].text.lower()
        range_._.data['group'] = REPLACE.get(per_count_, per_count_)


@spacy.registry.misc(COUNT[1]['after_match']['func'])
def count_word(ent):
    """Enrich the match with data."""
    ent._.new_label = 'count'
    word = [e for e in ent.ents if e.label_ == 'count_word'][0]
    word._.data = {'low': to_positive_int(REPLACE[word.text])}
    word._.new_label = 'count'


def range_values(ent):
    """Extract values from the range and cached label."""
    data = {}
    range_ = [e for e in ent.ents if e._.cached_label.split('.')[0] == 'range'][0]

    values = re.findall(FLOAT_RE, range_.text)

    if not all([re.search(INT_TOKEN_RE, v) for v in values]):
        raise RejectMatch

    keys = range_.label_.split('.')[1:]
    for key, value in zip(keys, values):
        data[key] = to_positive_int(value)

    range_._.data = data
    range_._.new_label = 'count'
    return range_
