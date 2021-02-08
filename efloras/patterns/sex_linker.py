"""Link traits to body subparts."""

from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes.dependency import NEAREST_ANCHOR

from efloras.pylib.const import TRAITS
from efloras.pylib.util import trim_traits

TRAITS_ = trim_traits(TRAITS, 'sex')

SEX_LINKER = DependencyPatterns(
    'sex_linker',
    on_match={
        'func': NEAREST_ANCHOR,
        'kwargs': {'anchor': 'sex'}
    },
    decoder={
        'sex': {'ENT_TYPE': 'sex'},
        'trait': {'ENT_TYPE': {'IN': TRAITS_}},
        'count': {'ENT_TYPE': 'count'},
        'part': {'ENT_TYPE': 'part'},
        'link': {'POS': {'IN': ['ADJ', 'AUX', 'VERB']}},
    },
    patterns=[
        'sex >> trait',
        'sex <  trait',
        'sex .  trait',
        'sex .  trait >> trait',
        'sex .  link  >> trait',
        'sex >  link  >> trait',
        'sex <  trait >> trait',
        'sex <  part  <  part',
        'sex ;  part  <  link >> trait',
    ],
)
