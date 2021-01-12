"""Patterns for attaching traits to plant parts.

We're adding what plant part and subpart a trait is referring to. This uses
a separate matcher object from the others because we're not merging tokens but
modifying them by adding the part and subpart fields.
"""

from traiter.util import DotDict

from ..matchers.descriptor import DESCRIPTOR_LABELS
from ..pylib.consts import COMMA, DOT, LINK_STEP, TRAIT_STEP

PLANT_LEVEL_LABELS = set(DESCRIPTOR_LABELS)
WITH_WORDS = """ with having only into by """.split()
SKIP = ['', 'shape_leader', 'dimension', 'ender']

PLANT_TOKEN = DotDict({
    'ent_type_': 'part',
    '_': DotDict({'data': {'trait': 'part', 'part': 'plant'}})})


def part_to_trait(span, part):
    """Connect the part to the matched traits."""
    subpart = None
    for token in span:
        label = token.ent_type_
        if label in PLANT_LEVEL_LABELS:
            part = PLANT_TOKEN
            token._.data['part'] = 'plant'
        elif label == 'part':
            if token.i > span.start:
                augment_data(token, part)
            part = token
        elif label == 'subpart':
            subpart = token
            augment_data(token, part)
        elif label == 'ender':
            subpart = None
        elif label:
            part = part if part else PLANT_TOKEN
            augment_data(token, part, subpart)


def out_of_order(span, part):
    """Attach traits to a subpart."""
    subpart = [t for t in span if t.ent_type_ == 'subpart']
    subpart = subpart[0] if subpart else None
    token = [t for t in span if t.ent_type_ == 'part']
    if token:
        augment_data(token[0], part)
        part = token[0]
    with_clause(span, part, subpart)


def with_clause(span, part, subpart=None):
    """Attach traits to a subpart."""
    for token in span:
        label = token.ent_type_
        if label == 'part':
            augment_data(token, part)
            part = token
        elif label == 'subpart':
            augment_data(token, part)
            subpart = token
        elif token._.step == TRAIT_STEP:
            augment_data(token, part, subpart)


def attach_final_suffix(span, part):
    """Attach traits to a plant part."""
    for token in list(span)[::-1]:
        if token.ent_type_ == 'part':
            part = token
        elif token._.step == TRAIT_STEP:
            augment_data(token, part)


def augment_data(token, part, subpart=None):
    """Attach traits from the part to the current token."""
    data = {}
    if part:
        data = {k: v for k, v in part._.data.items()
                if k in ('sex', 'location', 'part') and v}
    if subpart:
        data['subpart'] = subpart._.data['subpart']

    if frag := token._.data.get('_subpart'):
        data['subpart'] = frag

    if frag := token._.data.get('_part'):
        data['part'] = frag

    token._.data = {**data, **token._.data}


LINK = {
    LINK_STEP: [
        {
            'label': 'with_clause',
            'on_match': out_of_order,
            'priority': 10,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': ['color', 'shape']}},
                    {'POS': {'IN': ['ADP']}},
                    {'ENT_TYPE': {'IN': ['subpart']}},
                ],
                [
                    {'LOWER': {'IN': WITH_WORDS}},
                    {'ENT_TYPE': {'IN': SKIP}, 'OP': '*'},
                    {'_': {'step': TRAIT_STEP}},
                    {'ENT_TYPE': {'IN': ['part', 'subpart']}},
                    {'_': {'step': TRAIT_STEP}, 'OP': '?'},
                    {'TEXT': {'IN': COMMA}, 'OP': '?'},
                    {'ENT_TYPE': 'part_location', 'OP': '?'},
                ],
                [
                    {'LOWER': {'IN': WITH_WORDS}},
                    {'ENT_TYPE': {'IN': SKIP}, 'OP': '*'},
                    {'_': {'step': TRAIT_STEP}},
                    {'ENT_TYPE': {'IN': ['part', 'subpart']}},
                    {'_': {'step': TRAIT_STEP}, 'OP': '?'},
                    {'TEXT': {'IN': COMMA}, 'OP': '?'},
                    {'ENT_TYPE': 'part_location', 'OP': '?'},
                    {'POS': {'IN': ['ADP']}, 'OP': '?'},
                    {'_': {'step': TRAIT_STEP}},
                ],
                [
                    {'LOWER': {'IN': WITH_WORDS}},
                    {'ENT_TYPE': {'IN': SKIP}, 'OP': '*'},
                    {'ENT_TYPE': {'NOT_IN': SKIP}},
                    {'POS': {'IN': ['CCONJ']}, 'OP': '?'},
                    {'ENT_TYPE': {'NOT_IN': SKIP}},
                    {'POS': {'IN': ['ADV', 'VERB', 'ADJ']}, 'OP': '*'},
                    {'ENT_TYPE': {'IN': ['subpart']}},
                ],
                [
                    {'ENT_TYPE': {'IN': ['color', 'woodiness']}},
                    {'ENT_TYPE': {'IN': ['part', 'subpart']}},
                ],
                [
                    {'LOWER': {'IN': WITH_WORDS}},
                    {'LOWER': 'a', 'OP': '?'},
                    {'ENT_TYPE': {'NOT_IN': ['part', 'subpart', 'ender']}},
                    {'POS': {'IN': ['CCONJ']}, 'OP': '?'},
                    {'ENT_TYPE': {'NOT_IN': ['part', 'subpart', 'ender']},
                     'OP': '?'},
                    {'POS': {'IN': ['ADV', 'ADJ']}, 'OP': '*'},
                    {'ENT_TYPE': {'IN': ['part', 'subpart']}},
                    {'POS': {'IN': ['ADP']}, 'OP': '?'},
                    {'_': {'step': TRAIT_STEP}},
                ],
            ],
        },
        {
            'label': 'with_clause',
            'on_match': with_clause,
            'priority': 10,
            'patterns': [
                [
                    {'LOWER': {'IN': WITH_WORDS}},
                    {'LOWER': 'a', 'OP': '?'},
                    {'ENT_TYPE': {'NOT_IN': ['part', 'subpart', 'ender']},
                     'OP': '*'},
                    {'ENT_TYPE': {'IN': ['part', 'subpart']}},
                    {'_': {'step': TRAIT_STEP}},
                ],
            ],
        },
        {
            'label': 'part_to_trait',
            'on_match': part_to_trait,
            'patterns': [
                [
                    {'ENT_TYPE': 'part', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'subpart', 'OP': '?'},
                    {'ENT_TYPE': {'NOT_IN': ['part']}, 'OP': '*'},
                ],
            ],
        },
        {
            'label': 'attach',
            'on_match': attach_final_suffix,
            'patterns': [
                [
                    {'LOWER': 'and'},
                    {'_': {'step': TRAIT_STEP}},
                    {'ENT_TYPE': 'part'},
                    {'TEXT': {'IN': DOT}},
                ],
            ],
        },
    ],
}
