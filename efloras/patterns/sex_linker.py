"""Link traits to body subparts."""

from traiter.dependency_compiler import DependencyCompiler
from traiter.pipes.dependency import NEAREST_ANCHOR

TRAITS = ' color color_mod count location part size shape sex subpart '.split()

COMPILE = DependencyCompiler({
    'sex': {'ENT_TYPE': 'sex'},
    'trait': {'ENT_TYPE': {'IN': TRAITS}},
    'count': {'ENT_TYPE': 'count'},
    'part': {'ENT_TYPE': 'part'},
    'link': {'POS': {'IN': ['ADJ', 'AUX', 'VERB']}},
})

SEX_LINKER = [
    {
        'label': 'sex_linker',
        'on_match': {
            'func': NEAREST_ANCHOR,
            'kwargs': {'anchor': 'sex', 'exclude': ''}
        },
        'patterns': COMPILE(
            'sex >> trait',
            'sex <  trait',
            'sex .  trait',
            'sex .  trait >> trait',
            'sex .  link  >> trait',
            'sex >  link  >> trait',
            'sex <  trait >> trait',
            'sex <  part  <  part',
            'sex ;  part  <  link >> trait',
        ),
    },
]
