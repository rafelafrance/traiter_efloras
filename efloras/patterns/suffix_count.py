"""Common suffix count snippets."""

import spacy
from traiter.const import CLOSE, OPEN, PLUS

from ..pylib.const import CATEGORY, REPLACE

SUFFIX_COUNT = [
    {
        'label': 'count',
        'on_match': 'suffix_count.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'range'},
                {'TEXT': {'IN': PLUS}, 'OP': '?'},
                {'ENT_TYPE': 'count_suffix'},
            ],
            [
                {'TEXT': {'IN': OPEN}},
                {'ENT_TYPE': 'range'},
                {'TEXT': {'IN': PLUS}, 'OP': '?'},
                {'ENT_TYPE': 'count_suffix'},
                {'TEXT': {'IN': CLOSE}},
            ],
        ],
    },
]


@spacy.registry.misc(SUFFIX_COUNT[0]['on_match'])
def suffix_count(span):
    """Enrich the match with data."""
    data = {}
    for token in span:
        label = token.ent_type_
        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}
        elif label == 'range':
            return
        elif label == 'count_suffix':
            value = token.lower_
            part = REPLACE.get(value, value)
            key = CATEGORY.get(value, '_subpart')
            data[key] = part
        elif token.text in PLUS:
            data['indefinite'] = True
    return data
