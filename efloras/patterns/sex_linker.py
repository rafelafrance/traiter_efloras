"""Link traits to body subparts."""

from traiter.pipes.dependency import NEAREST_LINKER

from .part_linker import POS, TRAITS

_TRAITS = TRAITS + 'part subpart'.split()

SEX_LINKER = [
    {
        'label': 'sex_linker',
        'after_match': {
            'func': NEAREST_LINKER,
            'kwargs': {'root': 'sex', 'exclude': ''}
        },
        'patterns': [
            # sex >> trait
            [
                {
                    'RIGHT_ID': 'sex',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'sex'},
                },
                {
                    'LEFT_ID': 'sex',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # sex < trait
            [
                {
                    'RIGHT_ID': 'sex',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'sex'},
                },
                {
                    'LEFT_ID': 'sex',
                    'REL_OP': '<',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # sex . trait
            [
                {
                    'RIGHT_ID': 'sex',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'sex'},
                },
                {
                    'LEFT_ID': 'sex',
                    'REL_OP': '.',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # sex . trait >> trait2
            [
                {
                    'RIGHT_ID': 'sex',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'sex'},
                },
                {
                    'LEFT_ID': 'sex',
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
            # sex . adj >> trait
            [
                {
                    'RIGHT_ID': 'sex',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'sex'},
                },
                {
                    'LEFT_ID': 'sex',
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
            # sex > adj >> trait
            [
                {
                    'RIGHT_ID': 'sex',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'sex'},
                },
                {
                    'LEFT_ID': 'sex',
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
            # sex < trait >> trait
            [
                {
                    'RIGHT_ID': 'sex',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'sex'},
                },
                {
                    'LEFT_ID': 'sex',
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
            # sex ; part < adj >> trait
            [
                {
                    'RIGHT_ID': 'sex',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'sex'},
                },
                {
                    'LEFT_ID': 'sex',
                    'REL_OP': ';',
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'POS': {'IN': POS}},
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
        ],
    },
]
