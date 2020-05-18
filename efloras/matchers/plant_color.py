"""Common color snippets."""

from traiter.util import as_list
from ..pylib.terms import DASH, REPLACE


def plant_color(span):
    """Enrich a color phrase match."""
    parts = {}
    for token in span:
        part = REPLACE.get(token.text, token.text)
        if part not in DASH:
            parts[part] = 1     # Sets do not preserve order but dicts do
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    return {'value': value}


PLANT_COLOR = {
    'name': 'plant_color',
    'trait_names': """caylx_color corolla_color flower_color fruit_color
        hypanthium_color petal_color sepal_color """.split(),
    'matchers': {
        'plant_color': {
            'on_match': plant_color,
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
