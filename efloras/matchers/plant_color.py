"""Common color snippets."""

from ..pylib.terms import DASH, REPLACE


def color(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) not in DASH}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    return dict(
        value=value,
        start=span.start_char,
        end=span.end_char,
        raw_value=span.text,
    )


PLANT_COLOR = {
    'name': 'color',
    'trait_names': """ calyx_color corolla_color flower_color fruit_color
        hypanthium_color petal_color sepal_color """.split(),
    'matchers': {
        'color': {
            'on_match': color,
            'patterns': [
                [
                    {'_': {'term': 'color_leader'}, 'OP': '?'},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'color'}, 'OP': '+'},
                    {'_': {'term': 'dash'}, 'OP': '?'},
                    {'_': {'term': 'color_follower'}, 'OP': '*'},
                ],
                [{'_': {'term': 'color_leader'}}],
            ],
        },
    }
}
