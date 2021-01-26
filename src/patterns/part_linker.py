"""Link traits to body parts."""

import spacy
from traiter.linker_utils import linker

TRAITS = ' color color_mod count '.split()
POS = ' ADJ VERB '.split()

PART_LINKER = [
    {
        'label': 'part_linker',
        'on_match': 'part_linker.v1',
        'patterns': [
            # part > trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
                {
                    'LEFT_ID': 'trait1',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait2',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
            ],
            # part > subpart
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
            ],
            # part . subpart
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '.',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
            ],
            # part . adj >> subpart
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
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
            ],
            # part > adj >> subpart
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
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
            ],
        ],
    },
]


@spacy.registry.misc(PART_LINKER[0]['on_match'])
def body_part_linker(_, doc, idx, matches):
    """Use an entity matcher for entity linking."""
    linker(_, doc, idx, matches, 'part')
