"""Common color snippets."""

import spacy
from traiter.consts import DASH

from ..pylib.consts import MISSING, REPLACE

SKIP = DASH + MISSING

COLOR = [
    {
        'label': 'color',
        'on_match': 'color.v1',
        'patterns': [
            [
                {'LOWER': {'IN': MISSING}, 'OP': '?'},
                {'ENT_TYPE': {'IN': ['color', 'color_mod']}, 'OP': '?'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': 'color', 'OP': '+'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': {'IN': ['color', 'color_mod']}, 'OP': '*'},
            ],
        ],
    },
]


@spacy.registry.misc(COLOR[0]['on_match'])
def color(ent):
    """Enrich a phrase match."""
    print(ent)
    data = {}
    if any(t for t in ent if t.lower_ in MISSING):
        data['missing'] = True
    color_parts = {r: 1 for t in ent if (r := REPLACE.get(t.text, t.text)) not in SKIP}
    value = '-'.join(color_parts.keys())
    data['color'] = REPLACE.get(value, value)
    ent._.data = data
