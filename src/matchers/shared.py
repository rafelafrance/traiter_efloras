"""Patterns share across matchers."""

from ..pylib.consts import CLOSE, DOT, GROUP_STEP, OPEN, SEMICOLON

SHARED = {
    GROUP_STEP: [
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
        {
            'label': 'ender',
            'patterns': [[{'TEXT': {'IN': DOT + SEMICOLON}}]]
        },
    ],
}
