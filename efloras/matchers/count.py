"""Common count snippets."""

from .shared import CROSS, DASH, NUMBER, OPEN, SLASH
from ..pylib.terms import REPLACE

_NO_COUNTS = CROSS + SLASH + DASH + OPEN + """ average side times """.split()
_NO_COUNT = set(_NO_COUNTS)

_PER_COUNTS = ['pair', 'pairs']
_PER_COUNT = set(_PER_COUNTS)


def count(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
        _relabel='count',
    )

    for token in span:
        label = token._.label

        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}

        elif token.lower_ in _PER_COUNT:
            data['as'] = REPLACE.get(token.lower_, token.lower_)

        else:
            return {}

    return data


COUNT = {
    'name': 'count',
    'matchers': [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'_': {'label': 'range'}},
                    {'LOWER': {'IN': _PER_COUNTS}, 'OP': '?'},
                ],
                [
                    {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                    {'_': {'label': 'range'}},
                    {'LOWER': {'IN': _PER_COUNTS}, 'OP': '?'},
                    {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                    {'LOWER': {'REGEX': NUMBER}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'not_a_count',
            'on_match': lambda x: {},
            'patterns': [
                [
                    {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                    {'_': {'label': 'range'}},
                    {'LOWER': {'IN': _PER_COUNTS}, 'OP': '?'},
                    {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                    {'_': {'label': 'length_units'}, 'OP': '?'},
                    {'_': {'label': 'range'}, 'OP': '?'},
                ],
            ],
        },
    ]
}
