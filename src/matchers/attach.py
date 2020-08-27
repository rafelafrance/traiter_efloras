"""Patterns for attaching traits to plant parts."""
import re

from ..matchers.descriptor import DESCRIPTOR_LABELS
from ..matchers.shared import CLOSE, DOT, OPEN, PLUS
from ..pylib.terms import CATEGORY, REPLACE
from ..pylib.util import LINK_STEP, TRAIT_STEP

PLANT_LEVEL_LABELS = set(DESCRIPTOR_LABELS)

LABEL = {
    'suffix_count': 'count',
    'count_phrase': 'count',
}


def augment_data(token, part):
    """Attach traits from the part to the current token."""
    if not part:
        return
    for key, value in part._.data.items():
        if key in ('sex', 'location'):
            token._.data[key] = value


def relabel_token(token, part, subpart=None):
    """Relabel the token's entity type."""
    label = LABEL.get(token.ent_type_, token.ent_type_)
    part = part._.data['part'] if part else 'plant'
    if subpart:
        subpart = subpart._.data.get('subpart')
    else:
        subpart = token._.data.get('_subpart')

    label = f'{part}_{subpart}_{label}' if subpart else f'{part}_{label}'
    label = re.sub(r'_([^_]+)_\1', r'_\1', label)
    label = re.sub(r'^([^_]+)_\1', r'\1', label)

    token.ent_type_ = label


def part_to_trait(span, part):
    """Connect the part to the matched traits."""
    subpart = None
    for token in span:
        label = token.ent_type_
        if label in PLANT_LEVEL_LABELS:
            relabel_token(token, None)
        elif label == 'subpart':
            subpart = token
            augment_data(token, part)
        elif label and label != 'part':
            relabel_token(token, part, subpart)
            augment_data(token, part)


def with_clause(span, part):
    """Attach traits to a subpart."""
    subpart = None
    for token in list(span)[::-1]:
        label = token.ent_type_
        if label == 'part':
            augment_data(token, part)
            part = token
        elif label == 'subpart':
            augment_data(token, part)
            subpart = token
        elif token._.step == TRAIT_STEP:
            relabel_token(token, part, subpart)
            augment_data(token, part)


def suffixed_count(span, part):
    """Enrich the match with data."""
    relabel_token(span[0], part)


ATTACH = {
    LINK_STEP: [
        {
            'label': 'part_to_trait',
            'on_match': part_to_trait,
            'patterns': [
                [
                    {'ENT_TYPE': 'part', 'OP': '?'},
                    {'ENT_TYPE': '', 'OP': '?'},
                    {'ENT_TYPE': 'subpart', 'OP': '?'},
                    {'ENT_TYPE': {'NOT_IN': ['part']}, 'OP': '+'},
                ],
            ],
        },
        {
            'label': 'with_clause',
            'on_match': with_clause,
            'priority': 10,
            'patterns': [
                [
                    {'LOWER': {'IN': ['with', 'having']}},
                    {'LOWER': 'a', 'OP': '?'},
                    {'POS': {'IN': ['NOUN', 'ADJ', 'ADV']}, 'OP': '*'},
                    {'_': {'step': TRAIT_STEP}},
                    {'ENT_TYPE': {'IN': ['part', 'subpart']}},
                ],
            ],
        },
        {
            'label': 'suffixed_count',
            'on_match': suffixed_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'suffix_count'},
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'LOWER': 'or'},
                    {'ENT_TYPE': 'count'},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'ENT_TYPE': 'suffix_count'},
                ],
            ],
        },
    ],
}


def attach_final_suffix(span):
    """Attach traits to a plant part."""
    data = {}
    part, relabel = '', ''
    for token in list(span)[::-1]:
        if token.ent_type_ == 'part':
            part = token._.data['part']
        elif token._.step == TRAIT_STEP:
            data = token._.data
            relabel = f'{part}_{token.ent_type_}'
        data['_relabel'] = relabel
    data['_attached'] = True
    return data


def attach_retokenize(span):
    """Attach traits to a subpart."""
    label, subpart = '', ''
    data = {'_subpart_attached': True}
    for token in list(span):
        if token.ent_type_ == 'subpart':
            subpart = token._.data['subpart']
        elif token._.step == TRAIT_STEP:
            data = token._.data
            label = token.ent_type_
    data['_relabel'] = f'{subpart}_{label}'
    return data


def word_count(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
        low=int(REPLACE[span.lower_]),
    )
    if category := CATEGORY.get(span.lower_):
        data['_relabel'] = f'{category}_count'

    return data


OLD_ATTACH = {
    LINK_STEP: [
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
        {
            'label': 'attach_retokenize',
            'on_match': attach_retokenize,
            'patterns': [
                [
                    {'LOWER': {'IN': ['with', 'having']}},
                    {'LOWER': 'a', 'OP': '?'},
                    {'POS': {'IN': ['NOUN', 'ADJ', 'ADV']}, 'OP': '*'},
                    {'ENT_TYPE': 'subpart'},
                    {'_': {'step': TRAIT_STEP}},
                ],
            ],
        },
        {
            'label': 'suffixed_count',
            'on_match': suffixed_count,
            'patterns': [
                [
                    {'TEXT': {'IN': OPEN}, 'OP': '?'},
                    {'ENT_TYPE': 'count'},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'ENT_TYPE': 'suffix_count'},
                    {'TEXT': {'IN': CLOSE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'LOWER': 'or'},
                    {'ENT_TYPE': 'count'},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'ENT_TYPE': 'suffix_count'},
                ],
            ],
        },
        {
            'label': 'word_count',
            'on_match': word_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'count_phrase'},
                ],
            ],
        },
    ],
}
