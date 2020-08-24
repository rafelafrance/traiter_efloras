"""Patterns for attaching traits to plant parts."""

from ..matchers.shared import CLOSE, DOT, OPEN, PLUS
from ..pylib.terms import CATEGORY, REPLACE
from ..pylib.util import ATTACH_STEP, TRAIT_STEP


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


def suffixed_count(span):
    """Enrich the match with data."""
    data = {}
    subpart = {}

    for token in span:
        label = token.ent_type_

        if label == 'count':
            data = {**token._.data, **data}

        elif label == 'suffix_subpart':
            subpart = token._.data['_subpart']
            relabel = f'{REPLACE[token.lower_]}_count'
            data['_relabel'] = relabel

        elif token.text in PLUS:
            data['indefinite'] = True

    data['_subpart_attached'] = True
    data['_subpart'] = subpart

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


ATTACH = {
    ATTACH_STEP: [
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
                    {'ENT_TYPE': 'suffix_subpart'},
                    {'TEXT': {'IN': CLOSE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'count'},
                    {'LOWER': 'or'},
                    {'ENT_TYPE': 'count'},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'ENT_TYPE': 'suffix_subpart'},
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
