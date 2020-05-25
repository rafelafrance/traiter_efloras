"""Common color snippets."""

from traiter.util import to_positive_int

from .shared import RANGE_GROUPS


def count(span):
    """Enrich a phrase match."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    value = {}
    for token in span:
        label = token._.label

        if label in ('min', 'low', 'high', 'max'):
            if (as_int := to_positive_int(token.text)) is None:
                return {}
            value[label] = as_int

        elif label in ('cross', 'length_units', 'slash', 'dash'):
            return {}

    data['value'] = value

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
                    {'_': {'label': {'IN': ['cross', 'slash']}},
                     'OP': '?'},
                    {'_': {'label': 'min'}, 'OP': '?'},
                    {'_': {'label': 'low'}},
                    {'_': {'label': 'high'}, 'OP': '?'},
                    {'_': {'label': 'max'}, 'OP': '?'},
                    {'_': {'label': {
                        'IN': ['cross', 'length_units', 'slash', 'dash']}},
                        'OP': '?'},
                    {'_': {'label': {'IN': ['min', 'low', 'high', 'max']}},
                     'OP': '?'},
                ],
            ],
        },
    ]
}
