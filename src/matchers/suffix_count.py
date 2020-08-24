"""Common suffix count snippets."""

from ..pylib.terms import CATEGORY, REPLACE
from ..pylib.util import TRAIT_STEP


def suffix_subpart(span):
    """Enrich the match with data."""
    data = {}

    for token in span:
        if token.ent_type_ == 'count_suffix':
            data['_subpart'] = {
                'subpart': REPLACE[token.lower_],
                'start': token.idx,
                'end': token.idx + len(token),
            }

    return data


def count_phrase(span):
    """Enrich the match with data."""
    return {
        'low': REPLACE.get(span.text, span.text),
        'subpart': CATEGORY.get(span.text, span.text),
    }


SUFFIX_COUNT = {
    TRAIT_STEP: [
        {
            'label': 'suffix_subpart',
            'on_match': suffix_subpart,
            'patterns': [
                [
                    {'ENT_TYPE': 'count_suffix'},
                ],
            ],
        },
        {
            'label': 'count_phrase',
            'on_match': count_phrase,
            'patterns': [
                [
                    {'ENT_TYPE': 'count_word'},
                ],
            ],
        },
    ],
}
