"""Shared patterns."""

RANGE_GROUPS = {
    'min': [[
            {'_': {'label': 'open'}},
            {'_': {'label': 'number'}},
            {'_': {'label': {'IN': ['dash', 'prep', 'conj']}}},
            {'_': {'label': 'close'}},
        ]],
    'low': [[{'_': {'label': 'number'}}]],
    'high': [[
            {'_': {'label': {'IN': ['dash', 'prep']}}},
            {'_': {'label': 'number'}},
        ]],
    'max': [[
            {'_': {'label': 'open'}},
            {'_': {'label': {'IN': ['dash', 'prep', 'conj']}}},
            {'_': {'label': 'number'}},
            {'_': {'label': 'close'}},
]]}
