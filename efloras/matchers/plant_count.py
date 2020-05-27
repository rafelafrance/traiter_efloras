"""Common color snippets."""

from traiter.util import to_positive_int

from .shared import RANGE_GROUPS


NO_COUNT = """ cross length_units slash dash no_count """.split()


def count(span):
    """Enrich a phrase match."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label

        if label in ('min', 'low', 'high', 'max'):
            if (as_int := to_positive_int(token.text)) is None:
                return {}
            data[label] = as_int

        elif label in NO_COUNT:
            return {}

    return data


PLANT_COUNT = {
    'name': 'count',
    'groupers': RANGE_GROUPS,
    'matchers': [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'_': {'label': {'IN': ['cross', 'slash', 'no_count']}},
                     'OP': '?'},
                    {'_': {'label': 'min'}, 'OP': '?'},
                    {'_': {'label': 'low'}},
                    {'_': {'label': 'high'}, 'OP': '?'},
                    {'_': {'label': 'max'}, 'OP': '?'},
                    {'_': {'label': {'IN': NO_COUNT}}, 'OP': '?'},
                    {'_': {'label': {'IN': ['min', 'low', 'high', 'max']}},
                     'OP': '?'},
                ],
            ],
        },
    ]
}
