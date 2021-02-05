"""Link traits to body subparts."""

from traiter.const import DASH
from traiter.dependency_compiler import DependencyCompiler
from traiter.pipes.dependency import NEAREST_ANCHOR

TRAITS = ' color color_mod count location margin_shape size shape sex '.split()

COMPILE = DependencyCompiler({
    'subpart': {'ENT_TYPE': 'subpart'},
    'part': {'ENT_TYPE': 'part'},
    'trait': {'ENT_TYPE': {'IN': TRAITS}},
    'count': {'ENT_TYPE': 'count'},
    'dash': {'TEXT': {'IN': DASH}},
    'link': {'POS': {'IN': ['ADJ', 'AUX', 'VERB']}},
})

SUBPART_LINKER = [
    {
        'label': 'subpart_linker',
        'on_match': {
            'func': NEAREST_ANCHOR,
            'kwargs': {'anchor': 'subpart', 'exclude': 'part'}
        },
        'patterns': COMPILE(
            'subpart ; dash ; count',
            'subpart >> trait',
            'subpart <  trait',
            'subpart .  trait',
            'subpart .  trait >> trait',
            'subpart .  link  >> trait',
            'subpart >  link  >> trait',
            'subpart <  trait >> trait',
            'subpart ;  part  <  link >> trait',
        ),
     },
]
