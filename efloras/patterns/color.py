"""Common color snippets."""

import re

import spacy
from traiter.const import DASH

from ..pylib.const import MISSING, REMOVE, REPLACE

TEMP = ['\\' + c for c in DASH[:2]]
MULTIPLE_DASHES = fr'[{"".join(TEMP)}]{{2,}}'

SKIP = DASH + MISSING
COLOR_ENTS = ['color', 'color_mod']

COLOR = [
    {
        'label': 'color',
        'on_match': 'color.v1',
        'patterns': [
            [
                {'LOWER': {'IN': MISSING}, 'OP': '?'},
                {'ENT_TYPE': {'IN': COLOR_ENTS}, 'OP': '?'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': 'color', 'OP': '+'},
                {'TEXT': {'IN': DASH}, 'OP': '?'},
                {'ENT_TYPE': {'IN': COLOR_ENTS}, 'OP': '*'},
            ],
        ],
    },
]


@spacy.registry.misc(COLOR[0]['on_match'])
def color(ent):
    """Enrich a phrase match."""
    data = {}
    if any(t for t in ent if t.lower_ in MISSING):
        data['missing'] = True
    color_parts = {r: 1 for t in ent if (r := REPLACE.get(t.text, t.text))
                   not in SKIP and not REMOVE.get(t.lower_)}
    value = '-'.join(color_parts.keys())
    value = re.sub(rf'\s*{MULTIPLE_DASHES}\s*', r'-', value)
    data['color'] = REPLACE.get(value, value)
    ent._.data = data
