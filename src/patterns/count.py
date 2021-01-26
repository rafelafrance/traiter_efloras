"""Common count snippets."""

import re

import spacy
from traiter.consts import CLOSE, CROSS, FLOAT_RE, INT_RE, OPEN, SLASH
from traiter.pipes.entity_data import REJECT_MATCH, RejectMatch
from traiter.util import to_positive_int

from ..pylib.consts import REPLACE

_NOT_COUNTS = (CROSS + SLASH + """ average side times days weeks by """.split())
_NOT_COUNT = set(_NOT_COUNTS)

_COUNT_KILLER = """
    metric_length imperial_length metric_mass imperial_mass """.split()

PARENS = OPEN + CLOSE

IS_RANGE = {'REGEX': '^range'}

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
        ],
    },
    {
        'label': '_not_a_count',
        'on_match': REJECT_MATCH,
        'patterns': [
            [
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': {'IN': _COUNT_KILLER}, 'OP': '?'},
            ],
            [
                {'ENT_TYPE': IS_RANGE, 'OP': '?'},
                {'LOWER': {'IN': _NOT_COUNTS}},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': {'IN': _COUNT_KILLER}, 'OP': '?'},
            ],
            [
                {'ENT_TYPE': IS_RANGE},
                {'LOWER': {'IN': _NOT_COUNTS}},
                {'ENT_TYPE': IS_RANGE, 'OP': '?'},
                {'ENT_TYPE': {'IN': _COUNT_KILLER}, 'OP': '?'},
            ],
        ],
    },
]


@spacy.registry.misc(COUNT[0]['on_match'])
def count(ent):
    """Enrich the match with data."""
    data = {}

    for token in ent:
        label = token._.label_cache.split('.')[0]

        if label == 'range':
            fields = token._.label_cache.split('.')[1:]
            values = re.findall(FLOAT_RE, ent.text)
            all_ints = all([re.search(INT_RE, v) for v in values])
            if not all_ints:
                raise RejectMatch
            for field, value in zip(fields, values):
                data[field] = to_positive_int(value)

        elif label == 'per_count':
            data['group'] = REPLACE.get(token.lower_, token.lower_)

    ent._.data = data
