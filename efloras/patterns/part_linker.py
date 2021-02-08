"""Link traits to body parts."""

from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes.dependency import NEAREST_ANCHOR

from efloras.pylib.const import TRAITS
from efloras.pylib.util import trim_traits

TRAITS_ = trim_traits(TRAITS, 'part')
POS = ' ADJ VERB '.split()

PART_LINKER = DependencyPatterns(
    'part_linker',
    on_match={
        'func': NEAREST_ANCHOR,
        'kwargs': {'anchor': 'part'}
    },
    decoder={
        'part': {'ENT_TYPE': 'part'},
        'trait': {'ENT_TYPE': {'IN': TRAITS_}},
        'adv': {'POS': {'IN': ['ADV']}},
        'link': {'POS': {'IN': ['ADJ', 'AUX', 'VERB']}},
        'subpart': {'ENT_TYPE': 'subpart'},
    },
    patterns=[
        'part <  trait',
        'part .  trait',
        'part >> trait',
        'part .  trait >> trait',
        'part .  link  >> trait',
        'part <  link  >> trait',
        'part >  link  >> trait',
        'part <  trait >> trait',
        'part .  adv   .  trait',
        'part < subpart < trait',
    ],
)
