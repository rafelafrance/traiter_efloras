"""Parse the trait."""

from ..pylib.terms import REPLACE


def shape(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) and t._.term == 'shape'}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    return dict(
        value=value,
        start=span.start_char,
        end=span.end_char,
        raw_value=span.text,
    )


def location(span):
    """Enrich a phrase match."""
    return dict(
        value=span.text.lower(),
        start=span.start_char,
        end=span.end_char,
        raw_value=span.text,
    )


SHAPE_TRAITS = """ caylx_shape corolla_shape flower_shape hypanthium_shape
        leaf_shape petal_shape petiole_shape sepal_shape """.split()

PLANT_SHAPE = {
    'name': 'shape',
    'trait_names': SHAPE_TRAITS,
    'aux_names': [n.replace('_shape', '_location') for n in SHAPE_TRAITS],
    'matchers': {
        'shape': {
            'on_match': shape,
            'patterns': [
                [
                    {'_': {'term': {'IN': ['shape', 'shape_leader']}},
                     'OP': '?'},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'shape'}, 'OP': '+'},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'shape'}, 'OP': '?'},
                ],
                [
                    {'_': {'term': 'shape_leader'}},
                    {'_': {'term': {'IN': ['prep', 'dash']}}},
                    {'_': {'term': {'IN': ['shape_leader']}}},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'shape'}, 'OP': '+'},
                ],
            ],
        },
        'location': {
            'on_match': location,
            'patterns': [
                [
                    {'_': {'term': 'part_location'}},
                ],
            ],
        },
    }
}
