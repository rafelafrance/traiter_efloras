"""Common count snippets."""

from .shared import CROSS, DASH, OPEN, PER_COUNT, PER_COUNTS, SLASH
from ..pylib.terms import REPLACE

_NO_COUNTS = (CROSS + SLASH + DASH + OPEN
              + """ average side times days weeks """.split())
_NO_COUNT = set(_NO_COUNTS)

_COUNT_KILLER = """ length_units mass_units """.split()


def count(span):
    """Enrich the match with data."""
    data = dict(_relabel='count')

    for token in span:
        label = token._.label

        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}

        elif token.lower_ in PER_COUNT:
            data['group'] = REPLACE.get(token.lower_, token.lower_)

        else:
            return {}

    return data


def not_a_count(span):
    """Flag this as a token to be deleted."""
    for token in span:
        token._.aux['skip'] = True
    return {}


COUNT = {
    'name': 'count',
    'matchers': [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'_': {'label': 'range'}},
                    {'LOWER': {'IN': PER_COUNTS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'not_a_count',
            'on_match': not_a_count,
            'patterns': [
                [
                    {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                    {'_': {'label': 'range'}},
                    {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                    {'_': {'label': {'IN': _COUNT_KILLER}}, 'OP': '?'},
                    {'_': {'label': 'range'}, 'OP': '?'},
                ],
            ],
        },
    ]
}
