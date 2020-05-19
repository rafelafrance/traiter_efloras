"""Parse the trait."""

from traiter.util import DotDict as Trait

from ..pylib.terms import REPLACE


def shape(span):
    """Enrich a color phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) and t._.term == 'shape'}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    return Trait(
        value=value,
        start=span.start_char,
        end=span.end_char,
        raw_value=span.text,
    )


PLANT_SHAPE = {
    'name': 'shape',
    'trait_names': """caylx_shape corolla_shape flower_shape hypanthium_shape
        leaf_shape petal_shape petiole_shape sepal_shape """.split(),
    'matchers': {
        'shape': {
            'on_match': shape,
            'patterns': [
                [
                    {'_': {'term': {'IN': ['shape', 'shape_leader']}},
                     'OP': '?'},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'shape'}, 'OP': '+'},
                ],
                [
                    {'_': {'term': {'IN': ['shape', 'shape_leader']}},
                     'OP': '?'},
                    {'_': {'term': {'IN': ['dash', 'prep']}}, 'OP': '?'},
                    {'_': {'term': {'IN': ['shape', 'shape_leader']}},
                     'OP': '?'},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'shape'}, 'OP': '+'},
                ],
            ],
        },
    }
}
