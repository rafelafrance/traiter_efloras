"""Common color snippets."""

import re

from traiter.const import DASH
from traiter.patterns.matcher_patterns import MatcherPatterns

from efloras.pylib.const import COMMON_PATTERNS, MISSING, REMOVE, REPLACE

TEMP = ['\\' + c for c in DASH[:2]]
MULTIPLE_DASHES = fr'[{"".join(TEMP)}]{{2,}}'

SKIP = DASH + MISSING


def color(ent):
    """Enrich a phrase match."""
    parts = {r: 1 for t in ent
             if (r := REPLACE.get(t.lower_, t.lower_)) not in SKIP
             and not REMOVE.get(t.lower_)}
    value = '-'.join(parts.keys())
    value = re.sub(rf'\s*{MULTIPLE_DASHES}\s*', r'-', value)
    ent._.data['color'] = REPLACE.get(value, value)
    if any(t for t in ent if t.lower_ in MISSING):
        ent._.data['missing'] = True


COLOR = MatcherPatterns(
    'color',
    on_match=color,
    decoder=COMMON_PATTERNS | {
        'color_words': {'ENT_TYPE': {'IN': ['color', 'color_mod']}},
        'color': {'ENT_TYPE': 'color'},
    },
    patterns=[
        'missing? color_words* -* color+ -* color_words*',
    ],
)
