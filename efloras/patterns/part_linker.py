"""Link traits to body parts."""

from traiter.pipes.dependency import NEAREST_LINKER

TRAITS = ' color color_mod count location size shape '.split()

POS = ' ADJ VERB '.split()

_TRAITS = TRAITS + ' subpart '.split()


PART_LINKER = [
    {
        'label': 'part_linker',
        'after_match': {
            'func': NEAREST_LINKER,
            'kwargs': {'root': 'part', 'exclude': ''}
        },
        'patterns': [
            # part >> trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # part < trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '<',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # part . trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '.',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # part . trait >> trait2
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '.',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
                {
                    'LEFT_ID': 'trait1',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait2',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # part . adj >> trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '.',
                    'RIGHT_ID': 'adj1',
                    'RIGHT_ATTRS': {'POS': {'IN': POS}},
                },
                {
                    'LEFT_ID': 'adj1',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # part < adj >> trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '<',
                    'RIGHT_ID': 'adj1',
                    'RIGHT_ATTRS': {'POS': {'IN': POS}},
                },
                {
                    'LEFT_ID': 'adj1',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # part > adj >> trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '>',
                    'RIGHT_ID': 'adj1',
                    'RIGHT_ATTRS': {'POS': {'IN': POS}},
                },
                {
                    'LEFT_ID': 'adj1',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # part < trait >> trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '<',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
                {
                    'LEFT_ID': 'trait1',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait2',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
        ],
    },
]
