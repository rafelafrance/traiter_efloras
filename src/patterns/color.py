"""Common color snippets."""

import re

import spacy
from traiter.consts import DASH, DASH_RE
from traiter.pipes.entity_data import REJECT_MATCH

from ..pylib.consts import MISSING, REPLACE, REMOVE

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
    {
        'label': 'color_mod',
        'on_match': REJECT_MATCH,
        'patterns': [
            [
                {'ENT_TYPE': 'color_mod', 'OP': '+'},
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
    color_parts = {r: 1 for t in ent if (r := REPLACE.get(t.text, t.text))
                   not in SKIP and not REMOVE.get(t.lower_)}
    value = '-'.join(color_parts.keys())
    value = re.sub(rf'\s*{DASH_RE}+\s*', r'-', value)
    data['color'] = REPLACE.get(value, value)
    ent._.data = data
