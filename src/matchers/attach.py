"""Patterns for attaching traits to plant parts."""

from ..matchers.descriptor import DESCRIPTOR_LABELS
from ..matchers.shared import DOT, COMMA
from ..pylib.util import LINK_STEP, TRAIT_STEP

PLANT_LEVEL_LABELS = set(DESCRIPTOR_LABELS)
AUGMENT = ('sex', 'location')
SUBPART_END = {';', '.'}
SUBPART_ONCE = {'size'}

LABEL = {
    'suffix_count': 'count',
    'count_phrase': 'count',
}


def augment_data(token, part):
    """Attach traits from the part to the current token."""
    if not part:
        return
    data = {k: v for k, v in part._.data.items() if k in AUGMENT and v}
    token._.data = {**token._.data, **data}


def new_label(token, part, subpart=None):
    """Relabel the token's entity type."""
    label = LABEL.get(token.ent_type_, token.ent_type_)
    part = part._.data['part'] if part else 'plant'
    if subpart:
        subpart = subpart._.data.get('subpart')
    else:
        subpart = token._.data.get('_subpart')

    label = f'{part}_{subpart}_{label}' if subpart else f'{part}_{label}'
    label = {p: 1 for p in label.split('_')}
    label = '_'.join(p for p, _ in label.items())

    return label


def part_to_trait(span, part):
    """Connect the part to the matched traits."""
    subpart = None
    subpart_traits = set()
    for token in span:
        label = token.ent_type_
        if label in PLANT_LEVEL_LABELS:
            token.ent_type_ = new_label(token, None)
        elif label == 'part':
            if token.i > span.start:
                augment_data(token, part)
            part = token
        elif label == 'subpart':
            subpart = token
            augment_data(token, part)
        elif token.text in SUBPART_END:
            subpart = None
        elif label:
            trait = new_label(token, part, subpart)
            if subpart:
                if trait in subpart_traits:
                    subpart = None
                    subpart_traits = set()
                    trait = new_label(token, part, subpart)
                elif label in SUBPART_ONCE:
                    subpart_traits.add(trait)
            token.ent_type_ = trait
            augment_data(token, part)


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
            token.ent_type_ = new_label(token, part, subpart)
            augment_data(token, part)


def attach_final_suffix(span, part):
    """Attach traits to a plant part."""
    for token in list(span)[::-1]:
        if token.ent_type_ == 'part':
            part = token
        elif token._.step == TRAIT_STEP:
            token.ent_type_ = new_label(token, part)
            augment_data(token, part)


ATTACH = {
    LINK_STEP: [
        {
            'label': 'with_clause',
            'on_match': out_of_order,
            'priority': 10,
            'patterns': [
                [
                    {'LOWER': {'IN': ['with', 'having', 'only']}},
                    {'LOWER': 'a', 'OP': '?'},
                    {'POS': {'IN': ['NOUN', 'ADJ', 'ADV', 'VERB']}, 'OP': '*'},
                    {'_': {'step': TRAIT_STEP}},
                    {'ENT_TYPE': {'IN': ['part', 'subpart']}},
                    {'_': {'step': TRAIT_STEP}, 'OP': '?'},
                    {'TEXT': {'IN': COMMA}, 'OP': '?'},
                    {'ENT_TYPE': 'part_location', 'OP': '?'},
                    {'POS': {'IN': ['ADP']}, 'OP': '?'},
                    {'_': {'step': TRAIT_STEP}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'woodiness'},
                    {'ENT_TYPE': {'IN': ['part', 'subpart']}},
                ],
            ],
        },
        {
            'label': 'with_clause',
            'on_match': with_clause,
            'priority': 10,
            'patterns': [
                [
                    {'LOWER': {'IN': ['with', 'having', 'only']}},
                    {'LOWER': 'a', 'OP': '?'},
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
                    {'TEXT': {'IN': DOT}}
                ],
            ],
        },
    ],
}
