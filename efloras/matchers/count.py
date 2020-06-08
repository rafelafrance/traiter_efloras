"""Common count snippets."""

from traiter.util import to_positive_int  # pylint: disable=import-error

from .shared import RANGE_GROUPS
from ..pylib.terms import REPLACE

_NO_COUNT = """ cross length_units slash dash no_count """.split()


def count(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label

        if label in ('min', 'low', 'high', 'max'):
            if (as_int := to_positive_int(token.text)) is None:
                return {}
            if label == 'low' and data.get('low') is not None:
                data['high'] = as_int
            else:
                data[label] = as_int

        if label == 'suffix_label':
            data['suffix_label'] = True

        if label == 'per_count':
            data['as'] = REPLACE.get(token.lower_, token.lower_)

        elif label in _NO_COUNT:
            return {}

    return data


COUNT = {
    'name': 'count',
    'groupers': RANGE_GROUPS,
    'matchers': [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'_': {'label': 'low'}},
                    {'LOWER': 'or'},
                    {'_': {'label': 'low'}},
                    {'_': {'label': {'IN': _NO_COUNT}}, 'OP': '?'},
                    {'_': {'label': 'per_count'}, 'OP': '?'},
                ],
                [
                    {'_': {'label': {'IN': [
                        'cross', 'slash', 'no_count', 'with']}}, 'OP': '?'},
                    {'_': {'label': 'min'}, 'OP': '?'},
                    {'_': {'label': 'low'}},
                    {'_': {'label': 'high'}, 'OP': '?'},
                    {'_': {'label': 'max'}, 'OP': '?'},
                    {'_': {'label': {'IN': _NO_COUNT}}, 'OP': '?'},
                    {'_': {'label': 'per_count'}, 'OP': '?'},
                    {'_': {'label': {'IN': ['min', 'low', 'high', 'max']}},
                     'OP': '?'},
                ],
            ],
        },
    ]
}
