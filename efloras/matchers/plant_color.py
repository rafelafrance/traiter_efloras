"""Common color snippets."""

from ..pylib.catalog import DASH, REPLACE


def color_phrase(span):
    """Enrich a color phrase match."""
    parts = {}
    for token in span:
        part = REPLACE.get(token.text, token.text)
        if part not in DASH:
            parts[part] = 1     # Sets do not preserve order but dicts do
    value = '-'.join(parts)
    return {'value': REPLACE.get(value, value)}


PLANT_COLOR = {
    'color_phrase': {
        'on_match': color_phrase,
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
