"""Common count snippets."""

import re

import spacy
from traiter.const import CLOSE, CROSS, FLOAT_RE, INT_RE, OPEN, SLASH
from traiter.entity_data_util import REJECT_MATCH, RejectMatch
from traiter.util import to_positive_int

from ..pylib.const import IS_RANGE, REPLACE

NOT_COUNT_WORDS = CROSS + SLASH + """ average side times days weeks by """.split()

NOT_COUNT_ENTS = """ imperial_length metric_mass imperial_mass """.split()

COUNT = [
    {
        'label': 'count',
        'on_match': 'count.v1',
        'patterns': [
            [
                {'ENT_TYPE': IS_RANGE},
            ],
            [
                {'TEXT': {'IN': OPEN}},
                {'ENT_TYPE': IS_RANGE},
                {'TEXT': {'IN': CLOSE}},
            ],
        ],
    },
    {
        'label': 'per_count',
        'on_match': 'per_count.v1',
        'patterns': [
            [
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'per_count'},
            ],
            [
                {'ENT_TYPE': 'per_count'},
                {'LOWER': {'IN': ['of']}, 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
            ],
            [
                {'TEXT': {'IN': OPEN}},
                {'ENT_TYPE': IS_RANGE},
                {'TEXT': {'IN': CLOSE}},
                {'ENT_TYPE': 'per_count'},
            ],
        ],
    },
    {
        'label': 'count_word',
        'on_match': 'count_word.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'count_word'},
            ],
        ],
    },
    {
        'label': '_not_a_count',
        'on_match': REJECT_MATCH,
        'patterns': [
            [
                {'ENT_TYPE': IS_RANGE},
                {'LOWER': {'IN': NOT_COUNT_WORDS}},
                {'ENT_TYPE': IS_RANGE, 'OP': '?'},
                {'ENT_TYPE': {'IN': NOT_COUNT_ENTS}, 'OP': '?'},
            ],
        ],
    },
]


@spacy.registry.misc(COUNT[0]['on_match'])
def count(ent):
    """Enrich the match with data."""
    ent._.data = range_values(ent)


@spacy.registry.misc(COUNT[1]['on_match'])
def per_count(ent):
    """Enrich the match with data."""
    ent._.data = range_values(ent)

    if per_count_ := [t for t in ent if t._.cached_label == 'per_count']:
        per_count_ = per_count_[0].lower_
        ent._data['group'] = REPLACE.get(per_count_, per_count_)


def range_values(ent):
    """Extract values from the range and cached label."""
    data = {}
    values = re.findall(FLOAT_RE, ent.text)
    if not all([re.search(INT_RE, v) for v in values]):
        raise RejectMatch
    range_ = [t for t in ent if t._.cached_label.split('.')[0] == 'range'][0]
    keys = range_._.cached_label.split('.')[1:]
    for key, value in zip(keys, values):
        data[key] = to_positive_int(value)
    return data


@spacy.registry.misc(COUNT[2]['on_match'])
def count_word(ent):
    """Enrich the match with data."""
    word = [t.lower_ for t in ent if t._.cached_label == 'count_word']
    ent._.data['low'] = to_positive_int(REPLACE[word[0]])
    ent._.data['new_label'] = 'count'
