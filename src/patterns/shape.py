"""Parse shape traits."""

import re

import spacy
from traiter.const import DASH, DASH_RE

from ..pylib.const import IS_RANGE, REPLACE

MULTIPLE_DASHES = fr'{DASH_RE}{DASH_RE}+'
_DASH_TO = DASH + ['to']

SHAPE = [
    {
        'label': 'shape',
        'on_match': 'shape.v1',
        'patterns': [
            [
                {'ENT_TYPE': {'IN': ['shape', 'shape_leader', 'location']}, 'OP': '*'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': 'shape', 'OP': '+'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': 'shape', 'OP': '?'},
            ],
            [
                {'ENT_TYPE': 'shape_leader'},
                {'LOWER': {'IN': _DASH_TO}},
                {'ENT_TYPE': {'IN': [
                    'shape', 'shape_leader']}, 'OP': '+'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': {'IN': 'shape'}, 'OP': '+'},
            ],
            [
                {'ENT_TYPE': {'IN': ['shape', 'shape_leader']}, 'OP': '+'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': 'shape', 'OP': '+'},
            ],
        ],
    },
    {
        'label': 'n_shape',
        'on_match': 'n_shape.v1',
        'patterns': [
            [
                {'ENT_TYPE': {'IN': ['shape', 'shape_leader', 'location']}, 'OP': '*'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'shape_suffix'},
            ],
        ],
    },
]


@spacy.registry.misc(SHAPE[0]['on_match'])
def shape(ent):
    """Enrich a phrase match."""
    parts = {r: 1 for t in ent
             if (r := REPLACE.get(t.lower_, t.lower_))
             and t._.cached_label in {'shape', 'shape_suffix'}}
    parts = [REPLACE.get(p, p) for p in parts]
    value = '-'.join(parts)
    value = re.sub(MULTIPLE_DASHES, '-', value)
    value = REPLACE.get(value, value)
    data = dict(shape=value)
    loc = [t.lower_ for t in ent if t._.cached_label == 'location']
    if loc:
        data['location'] = loc[0]
    ent._.data = data


@spacy.registry.misc(SHAPE[1]['on_match'])
def n_shape(ent):
    """Handle 5-angular etc."""
    ent._.new_label = 'shape'
    ent._.data = {'shape': 'polygonal'}
