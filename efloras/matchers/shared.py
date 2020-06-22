"""Shared patterns."""

CLOSE = ' ) ] '.split()
CROSS = ' x × '.split()
DASH = '– - –– --'.split()
DOT = ' . '.split()
INT = r'^\d+$'
NUMBER = r'^\d+(\.\d*)?$'
OPEN = ' ( [ '.split()
PLUS = ' + '.split()
SLASH = ' / '.split()
QUOTE = ' " \' '.split()
LETTERS = 'abcdefghijklmnopqrstuvwxyz'.split()

PER_COUNTS = ['pair', 'pairs']
PER_COUNT = set(PER_COUNTS)


QUEST = {
    'name': 'range',
    'groupers': [
        {
            'label': 'quest',
            'patterns': [
                [
                    {'TEXT': {'IN': OPEN}},
                    {'TEXT': '?'},
                    {'TEXT': {'IN': CLOSE}},
                ],
                [{'LOWER': '?'}],
            ]
        },
    ],
}
