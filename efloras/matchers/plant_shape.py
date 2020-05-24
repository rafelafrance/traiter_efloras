"""Parse the trait."""

from ..pylib.terms import REPLACE


def shape(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) and t._.term == 'shape'}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    loc = [t.text.lower() for t in span if t._.term == 'part_location']
    trait = dict(
        value=value,
        start=span.start_char,
        end=span.end_char,
    )
    if loc:
        trait['location'] = loc[0]
    return trait


SHAPE_TRAITS = """ caylx_shape corolla_shape flower_shape hypanthium_shape
        leaf_shape petal_shape petiole_shape sepal_shape """.split()

PLANT_SHAPE = {
    'name': 'shape',
    'trait_names': SHAPE_TRAITS,
    'matchers': [
        {
            'label': 'shape',
            'on_match': shape,
            'patterns': [
                [
                    {'_': {'term': {'IN': [
                        'shape', 'shape_leader', 'part_location']}},
                     'OP': '*'},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'shape'}, 'OP': '+'},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'shape'}, 'OP': '?'},
                ],
                [
                    {'_': {'term': 'shape_leader'}},
                    {'_': {'term': {'IN': ['dash', 'prep']}}},
                    {'_': {'term': {'IN': ['shape_leader']}}},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'shape'}, 'OP': '+'},
                ],
            ],
        },
    ]
}
