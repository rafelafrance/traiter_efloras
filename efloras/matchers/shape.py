"""Parse the trait."""

from .shared import DASH
from ..pylib.terms import REPLACE
from ..pylib.util import TRAIT_STEP

_DASH_TO = DASH + ['to']


def shape(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) and t.ent_type_ == 'shape'}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    data = dict(shape=value)
    loc = [t.lower_ for t in span if t.ent_type_ == 'location']
    if loc:
        data['location'] = loc[0]
    return data


def n_shape(_):
    """Handle 5-angular etc."""
    data = {'shape': 'polygonal'}
    return data


SHAPE = {
    'name': 'shape',
    TRAIT_STEP: [
        {
            'label': 'shape',
            'on_match': shape,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': [
                        'shape', 'shape_leader', 'location']}, 'OP': '*'},
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
                    {'ENT_TYPE': 'shape', 'OP': '+'},
                ],
                [
                    {'ENT_TYPE': {'IN': [
                        'shape', 'shape_leader']}, 'OP': '+'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '+'},
                ],
            ],
        },
        {
            'label': 'shape.n',
            'on_match': n_shape,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': [
                        'shape', 'shape_leader', 'location']}, 'OP': '*'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'shape_suffix'},
                ],
            ],
        },
    ],
}
