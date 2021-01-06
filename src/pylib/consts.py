"""Project-wide constants."""

from pathlib import Path

from traiter.pylib.terms import Terms

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('floras') > -1 else Path.cwd().parent

DATA_DIR = BASE_DIR / 'data'

EFLORAS_DIR = DATA_DIR / 'eFloras'
EFLORAS_FAMILIES = DATA_DIR / 'efloras_families' / 'eFloras_family_list.csv'

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
SLASH = ' / / '.split()

PARTS = ['part', 'subpart']

TERM_PATH = BASE_DIR / 'src' / 'vocabulary' / 'terms.csv'
TERMS = Terms.read_csv(TERM_PATH)
TERMS += Terms.hyphenate_terms(TERMS)

REPLACE = TERMS.pattern_dicts('replace')
CATEGORY = TERMS.pattern_dicts('category')

PRESENCE = {
    'present': True,
    'presence': True,
    'absent': False,
    'absence': False,
}
PRESENT = list(PRESENCE)

ABBREVS = """Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec ca """

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
