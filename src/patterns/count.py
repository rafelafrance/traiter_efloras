"""Common count snippets."""

import spacy
from traiter.consts import CLOSE, CROSS, OPEN, SLASH
from traiter.pipes.entity_data import REJECT_MATCH

from ..pylib.consts import REPLACE

_NO_COUNTS = (CROSS + SLASH + """ average side times days weeks by """.split())
_NO_COUNT = set(_NO_COUNTS)

_COUNT_KILLER = """ metric_length mass_units """.split()

PARENS = OPEN + CLOSE

COUNT = [
    {
        'label': 'count',
        'on_match': 'count.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'range'},
                {'ENT_TYPE': 'per_count', 'OP': '?'},
            ],
            [
                {'ENT_TYPE': 'per_count'},
                {'LOWER': {'IN': ['of']}, 'OP': '?'},
                {'ENT_TYPE': 'range'},
            ],
            [
                {'TEXT': {'IN': OPEN}},
                {'ENT_TYPE': 'range'},
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
                {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                {'ENT_TYPE': 'range'},
                {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                {'ENT_TYPE': {'IN': _COUNT_KILLER}, 'OP': '?'},
                {'ENT_TYPE': 'range', 'OP': '?'},
            ],
        ],
    },
]


@spacy.registry.misc(COUNT[0]['on_match'])
def count(ent):
    """Enrich the match with data."""
    data = {}

    for token in ent:
        label = token.ent_type_

        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}

        elif label == 'per_count':
            data['group'] = REPLACE.get(token.lower_, token.lower_)

        elif token.lower_ in PARENS:
            continue

        elif token.lower_ in {'of'}:
            continue

        else:
            return

    return data
