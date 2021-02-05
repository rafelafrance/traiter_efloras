"""Link traits to body parts."""

from traiter.dependency_compiler import DependencyCompiler
from traiter.pipes.dependency import NEAREST_ANCHOR

TRAITS = ' color color_mod count location size shape sex subpart woodiness '.split()
POS = ' ADJ VERB '.split()

COMPILE = DependencyCompiler({
    'part': {'ENT_TYPE': 'part'},
    'trait': {'ENT_TYPE': {'IN': TRAITS}},
    'subpart': {'ENT_TYPE': 'subpart'},
    'adv':  {'POS': {'IN': ['ADV']}},
    'link': {'POS': {'IN': ['ADJ', 'AUX', 'VERB']}},
})

PART_LINKER = [
    {
        'label': 'part_linker',
        'on_match': {
            'func': NEAREST_ANCHOR,
            'kwargs': {'anchor': 'part', 'exclude': ''}
        },
        'patterns': COMPILE(
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
        ),
    },
]
