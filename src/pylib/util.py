"""Misc. utils."""

import re
from pathlib import Path

from traiter.pylib.util import to_positive_float
from traiter.spacy_nlp.terms import hyphenate_terms, read_terms

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('efloras') > -1 else Path.cwd().parent

DATA_DIR = BASE_DIR / 'data'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
LINK_STEP = 'link'

COLON = ' : '.split()
COMMA = ' , '.split()
DOT = ' . '.split()
INT = r'^\d+$'
NUMBER = r'^\d+(\.\d*)?$'
PLUS = ' + '.split()
SEMICOLON = ' ; '.split()
SLASH = ' / '.split()
NUMBER_RE = r'\d+(\.\d*)?'
INT_RE = r'\d+'

CROSS = ' x × '.split()
CROSS_RE = f'(?: {"|".join(CROSS)} )'

CLOSE = ' ) ] '.split()
CLOSE_RE = ['\\' + x for x in CLOSE]
CLOSE_RE = f'(?: {"|".join(CLOSE_RE)} )'

OPEN = ' ( [ '.split()
OPEN_RE = ['\\' + x for x in OPEN]
OPEN_RE = f'(?: {"|".join(OPEN_RE)} )'

DASH = '– - –– --'.split()
DASH_RE = f'(?: {"|".join(DASH)} )'

RANGE_RE = re.compile(
    rf"""
        (?: {OPEN_RE} (?P<min> {NUMBER_RE} ) {DASH_RE} {CLOSE_RE} )?
        (?P<low> {NUMBER_RE} )
        (?: {DASH_RE} (?P<high> {NUMBER_RE} ) )?
        (?: {OPEN_RE} {DASH_RE} (?P<max> {NUMBER_RE} ) {CLOSE_RE} )?
    """,
    flags=re.IGNORECASE | re.VERBOSE)

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

LENGTH_UNITS = [k for k in CONVERT.keys()]
LENGTH_UNITS += [f'{k}.' for k in CONVERT.keys()]
LENGTH_UNITS_RE = '|'.join([u.replace('.', '\\.') for u in LENGTH_UNITS])
LENGTH_UNITS_SET = set(LENGTH_UNITS)

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


def convert(number, units):
    """Normalize the units to meters."""
    return number * CONVERT.get(units, 1.0)


def range_(text):
    """Enrich a phrase match."""
    data = {}
    match = RANGE_RE.search(text)
    for key in ('min', 'low', 'high', 'max'):
        if (value := match.groupdict()[key]) is not None:
            data[key] = to_positive_float(value)
    return data
