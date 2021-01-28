"""Common count snippets."""

import re

import spacy
from traiter.const import CLOSE, CROSS, FLOAT_RE, INT_RE, OPEN, SLASH
from traiter.pipes.entity_data import REJECT_MATCH, RejectMatch
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
                {'ENT_TYPE': 'per_count', 'OP': '?'},
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
                {'ENT_TYPE': 'per_count', 'OP': '?'},
            ],
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
    data = {}

    if word := [t.lower_ for t in ent if t._.cached_label == 'count_word']:
        data['low'] = to_positive_int(REPLACE[word[0]])
        return

    values = re.findall(FLOAT_RE, ent.text)
    all_ints = all([re.search(INT_RE, v) for v in values])

    if not all_ints:
        raise RejectMatch

    range_ = [t for t in ent if t._.cached_label.split('.')[0] == 'range'][0]
    keys = range_._.cached_label.split('.')[1:]

    for key, value in zip(keys, values):
        data[key] = to_positive_int(value)

    if per_count := [t for t in ent if t._.cached_label == 'per_count']:
        per_count = per_count[0].lower_
        data['group'] = REPLACE.get(per_count, per_count)

    ent._.data = data
