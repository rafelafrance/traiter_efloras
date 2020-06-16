"""Common lobe count snippets."""

from .shared import PLUS
from ..pylib.terms import CATEGORY, REPLACE


def suffixed_count(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label

        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}

        elif label == 'suffix_count':
            relabel = f'{REPLACE[token.lower_]}_count'
            data['_relabel'] = relabel

        elif token.text in PLUS:
            data['indefinite'] = True

        else:
            return {}

    return data


def count_phrase(span):
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


SUFFIX_COUNT = {
    'name': 'lobe',
    'matchers': [
        {
            'label': 'suffixed_count',
            'on_match': suffixed_count,
            'patterns': [
                [
                    {'_': {'label': 'range'}},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'_': {'label': 'suffix_count'}}
                ],
            ],
        },
        {
            'label': 'count_phrase',
            'on_match': count_phrase,
            'patterns': [
                [
                    {'_': {'label': 'count_word'}}
                ],
            ],
        },
    ]
}
