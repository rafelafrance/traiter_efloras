"""Shared patterns."""

from ..pylib.util import GROUP_STEP

CLOSE = ' ) ] '.split()
COLON = ' : '.split()
COMMA = ' , '.split()
CROSS = ' x × '.split()
DASH = '– - –– --'.split()
DOT = ' . '.split()
INT = r'^\d+$'
NUMBER = r'^\d+(\.\d*)?$'
OPEN = ' ( [ '.split()
PLUS = ' + '.split()
SEMICOLON = ' ; '.split()
SLASH = ' / '.split()

PER_COUNTS = ['pair', 'pairs']
PER_COUNT = set(PER_COUNTS)

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
