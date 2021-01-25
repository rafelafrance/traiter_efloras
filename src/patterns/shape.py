"""Parse shape traits."""

import spacy
from traiter.consts import DASH

from ..pylib.consts import REPLACE

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
                {'ENT_TYPE': {'IN': [
                    'shape', 'shape_suffix']}, 'OP': '?'},
            ],
            [
                {'ENT_TYPE': 'shape_leader'},
                {'LOWER': {'IN': _DASH_TO}},
                {'ENT_TYPE': {'IN': [
                    'shape', 'shape_leader']}, 'OP': '+'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': {'IN': [
                    'shape', 'shape_suffix']}, 'OP': '+'},
            ],
            [
                {'ENT_TYPE': {'IN': ['shape', 'shape_leader']}, 'OP': '+'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': {'IN': ['shape', 'shape_suffix']}, 'OP': '+'},
            ],
        ],
    },
    {
        'label': 'shape',
        'on_match': 'n_shape.v1',
        'patterns': [
            [
                {'ENT_TYPE': {'IN': ['shape', 'shape_leader', 'location']}, 'OP': '*'},
                {'ENT_TYPE': 'range'},
                {'ENT_TYPE': 'shape_suffix'},
            ],
        ],
    },
]


@spacy.registry.misc(SHAPE[0]['on_match'])
def shape(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text))
             and t.ent_type_ in {'shape', 'shape_suffix'}}
    value = '-'.join(parts).replace('--', '-')
    value = REPLACE.get(value, value)
    data = dict(shape=value)
    loc = [t.lower_ for t in span if t.ent_type_ == 'location']
    if loc:
        data['location'] = loc[0]
    return data


@spacy.registry.misc(SHAPE[1]['on_match'])
def n_shape(_):
    """Handle 5-angular etc."""
    data = {'shape': 'polygonal'}
    return data
