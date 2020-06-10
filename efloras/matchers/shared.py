"""Shared patterns."""

CLOSE = [')', ']']
CROSS = ['x', '×']
DASH = ['–', '-', '––', '--']
INT = r'^\d+$'
NUMBER = r'^\d+(\.\d*)?$'
OPEN = ['(', '[']
SLASH = ['/']


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
