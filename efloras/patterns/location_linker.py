"""Link traits to body parts."""

from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes.dependency import NEAREST_ANCHOR

from efloras.pylib.const import TRAITS
from efloras.pylib.util import trim_traits

TRAITS_ = trim_traits(TRAITS, 'location')

LOCATION_LINKER = DependencyPatterns(
    'location_linker',
    on_match={
        'func': NEAREST_ANCHOR,
        'kwargs': {'anchor': 'location'}
    },
    decoder={
        'location': {'ENT_TYPE': 'location'},
        'trait': {'ENT_TYPE': {'IN': TRAITS_}},
        'link': {'POS': {'IN': ['ADJ', 'AUX', 'VERB']}},
    },
    patterns=[
        'location <  trait',
        'location .  trait',
        'location >> trait',
        'location .  trait >> trait',
        'location .  link  >> trait',
        'location <  link  >> trait',
        'location >  link  >> trait',
        'location <  trait >> trait',
    ],
)
