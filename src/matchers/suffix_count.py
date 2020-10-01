"""Common suffix count snippets."""

from traiter.pylib.util import to_positive_int  # pylint: disable=import-error

from ..pylib.util import CATEGORY, CLOSE, OPEN, PLUS, REPLACE, TRAIT_STEP


def suffix_count(span):
    """Enrich the match with data."""
    data = {}
    for token in span:
        label = token.ent_type_
        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}
        elif label == 'range':
            return {'_forget': True}
        elif label == 'count_suffix':
            value = token.lower_
            part = REPLACE.get(value, value)
            key = CATEGORY.get(value, '_subpart')
            data[key] = part
        elif token.text in PLUS:
            data['indefinite'] = True
    return data


def count_phrase(span):
    """Enrich the match with data."""
    return {
        'low': to_positive_int(REPLACE.get(span.text, span.text)),
        '_subpart': CATEGORY.get(span.text, span.text),
    }


SUFFIX_COUNT = {
    TRAIT_STEP: [
        {
            'label': 'count',
            'on_match': suffix_count,
            'patterns': [
                [
                    {'ENT_TYPE': 'range'},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'ENT_TYPE': 'count_suffix'},
                ],
                [
                    {'TEXT': {'IN': OPEN}},
                    {'ENT_TYPE': 'range'},
                    {'TEXT': {'IN': PLUS}, 'OP': '?'},
                    {'ENT_TYPE': 'count_suffix'},
                    {'TEXT': {'IN': CLOSE}},
                ],
            ],
        },
        {
            'label': 'count',
            'on_match': count_phrase,
            'patterns': [
                [
                    {'ENT_TYPE': 'count_word'},
                ],
            ],
        },
    ],
}
