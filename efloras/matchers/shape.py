"""Parse the trait."""

from .shared import DASH
from ..pylib.terms import REPLACE
from ..pylib.util import TRAIT_STEP

_DASH_TO = DASH + ['to']


def shape(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) and t._.label == 'shape'}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    data = dict(shape=value)
    loc = [t.lower_ for t in span if t._.label == 'location']
    if loc:
        data['location'] = loc[0]
    return data


def n_shape(_):
    """Handle 5-angular etc."""
    data = {'shape': 'polygonal', '_relabel': 'shape'}
    return data


SHAPE = {
    'name': 'shape',
    TRAIT_STEP: [
        {
            'label': 'shape',
            'on_match': shape,
            'patterns': [
                [
                    {'_': {'label': {'IN': [
                        'shape', 'shape_leader', 'location']}}, 'OP': '*'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'_': {'label': 'shape'}, 'OP': '+'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'_': {'label': 'shape'}, 'OP': '?'},
                ],
                [
                    {'_': {'label': 'shape_leader'}},
                    {'LOWER': {'IN': _DASH_TO}},
                    {'_': {'label': {'IN': [
                        'shape', 'shape_leader']}}, 'OP': '+'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'_': {'label': 'shape'}, 'OP': '+'},
                ],
                [
                    {'_': {'label': {'IN': [
                        'shape', 'shape_leader']}}, 'OP': '+'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'_': {'label': 'shape'}, 'OP': '+'},
                ],
            ],
        },
        {
            'label': 'n_shape',
            'on_match': n_shape,
            'patterns': [
                [
                    {'_': {'label': {'IN': [
                        'shape', 'shape_leader', 'location']}}, 'OP': '*'},
                    {'_': {'label': 'range'}},
                    {'_': {'label': 'shape_suffix'}},
                ],
            ],
        },
    ]
}
