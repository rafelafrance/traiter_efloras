"""Patterns for attaching traits to plant parts."""

from ..matchers.shared import CLOSE, DOT, OPEN, PLUS
from ..pylib.terms import CATEGORY, REPLACE
from ..pylib.util import ATTACH_STEP, TRAIT_STEP


def attach_final_suffix(span):
    """Attach traits to a plant part."""
    part = ''
    for token in list(span)[::-1]:
        if token._.label == 'part':
            part = token._.data['part']
        elif token._.step == TRAIT_STEP:
            token._.label = f'{part}_{token._.label}'
        token._.aux['attached'] = True
    return {'_retokenize': False}


def attach_retokenize(span):
    """Attach traits to a subpart."""
    label, subpart, data = '', '', {}
    for token in list(span):
        if token._.label == 'subpart':
            subpart = token._.data['subpart']
        elif token._.step == TRAIT_STEP:
            data = token._.data
            label = token._.label
        token._.aux['subpart_attached'] = True
    data['_relabel'] = f'{subpart}_{label}'
    return data


def suffixed_count(span):
    """Enrich the match with data."""
    data = {}
    subpart = {}

    for token in span:
        label = token._.label

        if label == 'count':
            data = {**token._.data, **data}

        elif label == 'suffix_subpart':
            subpart = token._.data['_subpart']
            relabel = f'{REPLACE[token.lower_]}_count'
            data['_relabel'] = relabel

        elif token.text in PLUS:
            data['indefinite'] = True

        token._.aux['subpart_attached'] = True

    for token in span:
        token._.aux['subpart'] = subpart

    return data


def word_count(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
        low=int(REPLACE[span.lower_]),
        _relabel='count',
    )
    if category := CATEGORY.get(span.lower_):
        data['_relabel'] = f'{category}_count'

    return data


ATTACH = {
    'name': 'attach',
    ATTACH_STEP: [
        {
            'label': 'attach',
            'on_match': attach_final_suffix,
            'patterns': [
                [
                    {'LOWER': 'and'},
                    {'_': {'step': TRAIT_STEP}},
                    {'_': {'label': 'part'}},
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
                    {'_': {'label': 'subpart'}},
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
                    {'_': {'label': 'count'}},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'_': {'label': 'suffix_subpart'}},
                    {'TEXT': {'IN': CLOSE}, 'OP': '?'},
                ],
                [
                    {'_': {'label': 'count'}},
                    {'LOWER': 'or'},
                    {'_': {'label': 'count'}},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'_': {'label': 'suffix_subpart'}},
                ],
            ],
        },
        {
            'label': 'word_count',
            'on_match': word_count,
            'patterns': [
                [
                    {'_': {'label': 'count_phrase'}},
                ],
            ],
        },
    ],
}
