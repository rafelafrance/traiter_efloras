"""Patterns share across patterns."""

from traiter.const import CLOSE, OPEN

SHARED = [
    {
        'label': 'quest',
        'patterns': [
            [{'TEXT': '?'}],
            [
                {'TEXT': {'IN': OPEN}},
                {'TEXT': '?'},
                {'TEXT': {'IN': CLOSE}},
            ],
        ]
    },
]
