"""Common color snippets."""

from ..pylib.terms import DASH, REPLACE
from .shared import DASH


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
    )


COLOR = {
    'name': 'color',
    'matchers': [
        {
            'label': 'color',
            'on_match': color,
            'patterns': [
                [
                    {'_': {'label': 'color_leader'}, 'OP': '?'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'_': {'label': 'color'}, 'OP': '+'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'_': {'label': 'color_follower'}, 'OP': '*'},
                ],
                [{'_': {'label': 'color_leader'}}],
            ],
        },
    ]
}
