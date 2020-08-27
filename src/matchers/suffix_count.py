"""Common suffix count snippets."""

from ..pylib.terms import CATEGORY, REPLACE
from ..pylib.util import TRAIT_STEP

from ..matchers.shared import CLOSE, OPEN, PLUS


def suffix_count(span):
    """Enrich the match with data."""
    data = {}
    for token in span:
        label = token.ent_type_
        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}
        elif label == 'range':
            return {'_skip': True}
        elif label == 'count_suffix':
            value = token.lower_
            data['_subpart'] = REPLACE.get(value, value)
    return data


def count_phrase(span):
    """Enrich the match with data."""
    return {
        'low': REPLACE.get(span.text, span.text),
        '_subpart': CATEGORY.get(span.text, span.text),
    }


SUFFIX_COUNT = {
    TRAIT_STEP: [
        {
            'label': 'suffix_count',
            'on_match': suffix_count,
            'patterns': [
                [
                    {'TEXT': {'IN': OPEN}, 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'ENT_TYPE': 'count_suffix'},
                    {'TEXT': {'IN': CLOSE}, 'OP': '?'},
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
