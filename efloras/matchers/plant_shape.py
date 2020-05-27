"""Parse the trait."""

from ..pylib.terms import REPLACE


def shape(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) and t._.label == 'shape'}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    loc = [t.lower_ for t in span if t._.label == 'part_location']
    trait = dict(
        value=value,
        start=span.start_char,
        end=span.end_char,
    )
    if loc:
        trait['location'] = loc[0]
    return trait


PLANT_SHAPE = {
    'name': 'shape',
    'matchers': [
        {
            'label': 'shape',
            'on_match': shape,
            'patterns': [
                [
                    {'_': {'label': {'IN': [
                        'shape', 'shape_leader', 'part_location']}},
                     'OP': '*'},
                    {'_': {'label': 'dash'}, 'OP': '?'},
                    {'_': {'label': 'shape'}, 'OP': '+'},
                    {'_': {'label': 'dash'}, 'OP': '?'},
                    {'_': {'label': 'shape'}, 'OP': '?'},
                ],
                [
                    {'_': {'label': 'shape_leader'}},
                    {'_': {'label': {'IN': ['dash', 'prep']}}},
                    {'_': {'label': {'IN': ['shape_leader']}}},
                    {'_': {'label': 'dash'}, 'OP': '?'},
                    {'_': {'label': 'shape'}, 'OP': '+'},
                ],
            ],
        },
    ]
}
