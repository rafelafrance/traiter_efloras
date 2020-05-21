"""Common color snippets."""

from traiter.util import to_positive_int


def count(span):
    """Enrich a phrase match."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
        raw_value=span.text,
    )

    value = {}
    for token in span:
        term = token._.term

        if term in ('min_count', 'low_count', 'high_count', 'max_count'):
            value[term] = to_positive_int(token.text)

        elif term in ('cross', 'length_units'):
            return {}

    data['value'] = value

    return data


PLANT_COUNT = {
    'name': 'count',
    'trait_names': """ ovary_count seed_count stamen_count """.split(),
    'groupers': {
        'min_count': [[
            {'_': {'term': 'open'}},
            {'_': {'term': 'int'}},
            {'_': {'term': {'IN': ['dash', 'conj', 'prep']}}},
            {'_': {'term': 'close'}},
        ]],
        'low_count': [[
            {'_': {'term': 'int'}},
        ]],
        'high_count': [[
            {'_': {'term': {'IN': ['dash', 'conj', 'prep']}}},
            {'_': {'term': 'int'}},
        ]],
        'max_count': [[
            {'_': {'term': 'open'}},
            {'_': {'term': {'IN': ['dash', 'conj', 'prep']}}},
            {'_': {'term': 'int'}},
            {'_': {'term': 'close'}},
        ]],
    },
    'matchers': [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'_': {'term': 'min_count'}, 'OP': '?'},
                    {'_': {'term': 'low_count'}},
                    {'_': {'term': 'high_count'}, 'OP': '?'},
                    {'_': {'term': 'max_count'}, 'OP': '?'},
                    {'_': {'term': {'IN': ['cross', 'length_units']}},
                     'OP': '?'},
                ],
            ],
        },
    ]
}
