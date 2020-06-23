"""Common color snippets."""

from ..pylib.terms import REPLACE
from .shared import DASH


def color(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) not in DASH}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    return dict(color=value)


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
                [
                    {'_': {'label': 'color_leader'}},
                    {'_': {'label': 'color_follower'}, 'OP': '*'},
                ],
            ],
        },
    ]
}
