"""Plant part parser."""

import re

import spacy
from traiter.consts import COLON
from traiter.util import FLAGS

from ..pylib.consts import REPLACE, TERMS

_PATTERNS = [t for t in TERMS if t['label'] == 'part']
_PATTERNS = sorted([str(t['pattern']) for t in _PATTERNS], key=len, reverse=True)

PATTERN_RE = '|'.join(_PATTERNS)
PATTERN_RE = re.compile(f'({PATTERN_RE})', FLAGS)

PART = [
    {
        'label': 'part',
        'on_match': 'part.v1',
        'patterns': [
            [
                {'ENT_TYPE': {
                    'IN': ['sex', 'sex_enclosed', 'location']}, 'OP': '*'},
                {'ENT_TYPE': 'part'},
            ],
            [
                {'ENT_TYPE': {'IN': ['part']}},
                {'ENT_TYPE': {'IN': ['sex', 'sex_enclosed', 'location']}},
            ],
            [
                {'ENT_TYPE': 'part'},
                {'TEXT': {'IN': COLON}, 'OP': '?'},
                {'ENT_TYPE': {'IN': ['sex']}},
            ],
            [
                {'ENT_TYPE': 'location'},
                {'ENT_TYPE': 'per_count', 'OP': '?'},
                {},
                {'ENT_TYPE': 'part'},
            ],
            [
                {'ENT_TYPE': 'location'},
                {'ENT_TYPE': 'per_count', 'OP': '?'},
                {'ENT_TYPE': 'part'},
            ],
        ],
    },
]


@spacy.registry.misc(PART[0]['on_match'])
def part(ent):
    """Enrich a plant part match."""
    data = {}

    for token in ent:
        label = token.ent_type_
        value = token.lower_
        if label == 'part':
            data['part'] = REPLACE.get(value, value)
        elif label in ('sex_enclosed', 'sex'):
            value = re.sub(r'\W+', '', token.lower_)
            data['sex'] = REPLACE.get(value, value)
        elif label == 'location':
            data['location'] = value
        elif label == 'per_count':
            data['group'] = REPLACE.get(token.lower_, token.lower_)

    ent._.data = data
