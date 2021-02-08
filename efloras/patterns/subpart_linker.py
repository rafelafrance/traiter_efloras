"""Link traits to body subparts."""

from traiter.const import DASH
from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes.dependency import NEAREST_ANCHOR

from efloras.pylib.const import TRAITS
from efloras.pylib.util import trim_traits

TRAITS_ = trim_traits(TRAITS, 'subpart')

SUBPART_LINKER = DependencyPatterns(
    'subpart_linker',
    on_match={
        'func': NEAREST_ANCHOR,
        'kwargs': {'anchor': 'subpart', 'exclude': 'part'}
    },
    decoder={
        'subpart': {'ENT_TYPE': 'subpart'},
        'part': {'ENT_TYPE': 'part'},
        'trait': {'ENT_TYPE': {'IN': TRAITS_}},
        'count': {'ENT_TYPE': 'count'},
        'dash': {'TEXT': {'IN': DASH}},
        'link': {'POS': {'IN': ['ADJ', 'AUX', 'VERB']}},
    },
    patterns=[
        'subpart ; dash ; count',
        'subpart >> trait',
        'subpart <  trait',
        'subpart .  trait',
        'subpart .  trait >> trait',
        'subpart .  link  >> trait',
        'subpart >  link  >> trait',
        'subpart <  trait >> trait',
        'subpart ;  part  <  link >> trait',
    ],
)
