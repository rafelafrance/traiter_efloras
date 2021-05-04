"""Parse shape traits."""

import re

from spacy import registry
from traiter.const import DASH
from traiter.patterns.matcher_patterns import MatcherPatterns

from efloras.pylib.const import COMMON_PATTERNS, REPLACE

TEMP = ['\\' + c for c in DASH[:2]]
MULTIPLE_DASHES = fr'[{"".join(TEMP)}]{{2,}}'

DECODER = COMMON_PATTERNS | {
    'shape': {'ENT_TYPE': 'shape'},
    'shape_leader': {'ENT_TYPE': 'shape_leader'},
    'shape_loc': {'ENT_TYPE': {'IN': ['shape', 'shape_leader', 'location']}},
    'shape_word': {'ENT_TYPE': {'IN': ['shape', 'shape_leader']}},
    'angular': {'LOWER': {'IN': ['angular', 'angulate']}},
}

SHAPE = MatcherPatterns(
    'shape',
    on_match='efloras.shape.v1',
    decoder=DECODER,
    patterns=[
        'shape_loc* -* shape+',
        'shape_loc* -* shape -* shape+',
        'shape_leader -/to shape_word+ -* shape+',
        'shape_word+ -* shape+',
    ],
)

N_SHAPE = MatcherPatterns(
    'n_shape',
    on_match='efloras.n_shape.v1',
    decoder=DECODER,
    patterns=[
        'shape_loc* 9 - angular',
    ],
)


@registry.misc(SHAPE.on_match)
def shape(ent):
    """Enrich a phrase match."""
    parts = {r: 1 for t in ent
             if (r := REPLACE.get(t.lower_, t.lower_))
             and t._.cached_label in {'shape', 'shape_suffix'}}
    value = '-'.join(parts.keys())
    value = re.sub(rf'\s*{MULTIPLE_DASHES}\s*', r'-', value)
    ent._.data['shape'] = REPLACE.get(value, value)
    loc = [t.lower_ for t in ent if t._.cached_label == 'location']
    if loc:
        ent._.data['location'] = loc[0]


@registry.misc(N_SHAPE.on_match)
def n_shape(ent):
    """Handle 5-angular etc."""
    ent._.new_label = 'shape'
    ent._.data = {'shape': 'polygonal'}
