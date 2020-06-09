"""Shared patterns."""

RANGE_GROUPS = [
    {
        'label': 'min',
        'patterns': [[
            {'_': {'label': 'open'}},
            {'_': {'label': 'number'}},
            {'_': {'label': {'IN': ['dash', 'prep', 'conj']}}},
            {'_': {'label': 'close'}},
        ]],
    },
    {
        'label': 'low',
        'patterns': [[
            {'_': {'label': 'number'}},
        ]],
    },
    {
        'label': 'high',
        'patterns': [[
            {'_': {'label': {'IN': ['dash', 'prep']}}},
            {'_': {'label': 'number'}},
        ]],
    },
    {
        'label': 'max',
        'patterns': [[
            {'_': {'label': 'open'}},
            {'_': {'label': {'IN': ['dash', 'prep', 'conj']}}},
            {'_': {'label': 'number'}},
            {'_': {'label': 'close'}},
        ]],
    },
]
