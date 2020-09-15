"""Common color snippets."""

from ..pylib.util import REPLACE, TRAIT_STEP
from .shared import DASH


def color(span):
    """Enrich a phrase match."""
    parts = {r: 1 for t in span
             if (r := REPLACE.get(t.text, t.text)) not in DASH}
    value = '-'.join(parts)
    value = REPLACE.get(value, value)
    return dict(color=value)


COLOR = {
    TRAIT_STEP: [
        {
            'label': 'color',
            'on_match': color,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': ['color', 'color_modifier']},
                     'OP': '?'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': 'color', 'OP': '+'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': {'IN': ['color', 'color_modifier']},
                     'OP': '*'},
                ],
            ],
        },
    ],
}
