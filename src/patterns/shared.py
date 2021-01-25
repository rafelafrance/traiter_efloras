"""Patterns share across patterns."""

from traiter.consts import CLOSE, OPEN

SHARED = [
    {
        'label': 'quest',
        'patterns': [
            [
                {'TEXT': {'IN': OPEN}},
                {'TEXT': '?'},
                {'TEXT': {'IN': CLOSE}},
            ],
            [{'TEXT': '?'}],
        ]
    },
]
