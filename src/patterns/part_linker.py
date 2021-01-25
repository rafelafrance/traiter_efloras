"""Link traits to body parts."""

import spacy
from traiter.linker_utils import linker


TRAITS = ' color color_mod '.split()
LINKERS = ' prep conj cc '.split()


PART_LINKER = [
    {
        'label': 'part_linker',
        'on_match': 'part_linker.v1',
        'patterns': [
            # part . linker
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
            # part . trait > trait2
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
                    'REL_OP': '>',
                    'RIGHT_ID': 'trait2',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
            ],
            # part . trait > trait2 > trait3
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
                    'REL_OP': '>',
                    'RIGHT_ID': 'trait2',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
                {
                    'LEFT_ID': 'trait2',
                    'REL_OP': '>',
                    'RIGHT_ID': 'trait3',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
            ],
            # part . adj > trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '.',
                    'RIGHT_ID': 'adj1',
                    'RIGHT_ATTRS': {'POS': {'IN': ['ADJ']}},
                },
                {
                    'LEFT_ID': 'adj1',
                    'REL_OP': '>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
            ],
            # part . adj > trait > trait
            [
                {
                    'RIGHT_ID': 'part',
                    'RIGHT_ATTRS': {'ENT_TYPE': 'part'},
                },
                {
                    'LEFT_ID': 'part',
                    'REL_OP': '.',
                    'RIGHT_ID': 'adj1',
                    'RIGHT_ATTRS': {'POS': {'IN': 'ADJ'}},
                },
                {
                    'LEFT_ID': 'adj1',
                    'REL_OP': '>',
                    'RIGHT_ID': 'trait1',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
                {
                    'LEFT_ID': 'trait1',
                    'REL_OP': '>',
                    'RIGHT_ID': 'trait2',
                    'RIGHT_ATTRS': {'ENT_TYPE': {'IN': TRAITS}},
                },
            ],
        ],
    },
]


@spacy.registry.misc(PART_LINKER[0]['on_match'])
def body_part_linker(_, doc, idx, matches):
    """Use an entity matcher for entity linking."""
    print(doc)
    print(matches)
    for i in matches[0][1]:
        print(doc[i])
    linker(_, doc, idx, matches, 'part')
