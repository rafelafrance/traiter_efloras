"""Parse the trait."""

from ..pylib.terms import REPLACE
from .shared import DASH

_DASH_TO = DASH + ['to']


def shape(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) and t._.label == 'shape'}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    trait = dict(shape=value)
    loc = [t.lower_ for t in span if t._.label == 'location']
    if loc:
        trait['location'] = loc[0]
    return trait


SHAPE = {
    'name': 'shape',
    'matchers': [
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
                    {'_': {'label': 'shape_leader'}},
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
    ]
}
