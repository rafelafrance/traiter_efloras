"""Link traits to body subparts."""

from traiter.const import DASH
from traiter.pipes.dependency import NEAREST_LINKER

from .part_linker import POS, TRAITS

_TRAITS = TRAITS

SUBPART_LINKER = [
    {
        'label': 'subpart_linker',
        'after_match': {
            'func': NEAREST_LINKER,
            'kwargs': {'root': 'subpart', 'exclude': 'part'}
        },
        'patterns': [
            # subpart ; dash ; count
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
                    'REL_OP': ';',
                    'RIGHT_ID': 'dash1',
                    'RIGHT_ATTRS': {'TEXT': {'IN': DASH}},
                },
                {
                    'LEFT_ID': 'dash1',
                    'REL_OP': ';',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'count'},
                },
            ],
            # subpart >> trait
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # subpart < trait
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
                    'REL_OP': '<',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # subpart . trait
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
                    'REL_OP': '.',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': _TRAITS}},
                },
            ],
            # subpart . trait >> trait2
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
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
            # subpart . adj >> trait
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
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
            # subpart > adj >> trait
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
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
            # subpart < trait >> trait
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
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
            # subpart ; part < adj >> trait
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
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
