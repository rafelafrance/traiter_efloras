"""Link traits to body subparts."""

import spacy
from traiter.linker_utils import linker

TRAITS = ' color color_mod count '.split()
LINKERS = ' prep conj cc '.split()
POS = ' ADJ VERB '.split()

SUBPART_LINKER = [
    {
        'label': 'subpart_linker',
        'on_match': 'subpart_linker.v1',
        'patterns': [
            # subpart > trait
            [
                {
                    'RIGHT_ID': 'subpart',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'subpart'},
                },
                {
                    'LEFT_ID': 'subpart',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
                {
                    'LEFT_ID': 'trait1',
                    'REL_OP': '>>',
                    'RIGHT_ID': 'trait2',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
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
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
            ],
        ],
    },
]


@spacy.registry.misc(SUBPART_LINKER[0]['on_match'])
def body_subpart_linker(_, doc, idx, matches):
    """Use an entity matcher for entity linking."""
    linker(_, doc, idx, matches, 'subpart', exclude='part')
