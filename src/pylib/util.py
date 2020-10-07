"""Misc. utils."""

from pathlib import Path

from traiter.spacy_nlp.terms import hyphenate_terms, read_terms

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('floras') > -1 else Path.cwd().parent

DATA_DIR = BASE_DIR / 'data'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
LINK_STEP = 'link'

CLOSE = ' ) ] '.split()
COLON = ' : '.split()
COMMA = ' , '.split()
CROSS = ' x × '.split()
DASH = '– - –– --'.split()
DOT = ' . '.split()
INT = r'^\d+$'
INT_RE = r'\d+'
NUMBER = r'^\d+(\.\d*)?$'
OPEN = ' ( [ '.split()
PLUS = ' + '.split()
SEMICOLON = ' ; '.split()
SLASH = ' / '.split()

TERM_PATH = BASE_DIR / 'src' / 'vocabulary' / 'terms.csv'
TERMS = read_terms(TERM_PATH)
TERMS += hyphenate_terms(TERMS)

REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}
CATEGORY = {t['pattern']: c for t in TERMS if (c := t.get('category'))}
ABBREVS = """Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec """

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

CONVERT = {
    'cm': 10.0,
    'dm': 100.0,
    'm': 1000.0,
    'mm': 1.0,
    'µm': 1.0e-3,
    'centimeters': 10.0,
    'decimeters': 100.0,
    'meters': 1000.0,
    'millimeters': 1.0,
}


def convert(number, units):
    """Normalize the units to meters."""
    return number * CONVERT.get(units, 1.0)
