"""Misc. utils."""
import re
from pathlib import Path

from traiter.pylib.terms import hyphenate_terms, read_terms
from traiter.pylib.util import FLAGS

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('efloras') > -1 else Path.cwd().parent

DATA_DIR = BASE_DIR / 'data'
VOCAB_DIR = BASE_DIR / 'src' / 'vocabulary'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
LINK_STEP = 'link'

TERM_PATH = VOCAB_DIR / 'terms.csv'
_QUOTE = """["']"""
TERMS = read_terms(TERM_PATH)
TERMS += hyphenate_terms(TERMS)
LABELS = sorted({t['label'] for t in TERMS})
REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}
CATEGORY = {t['pattern']: c for t in TERMS if (c := t.get('category'))}
PATTERN_RE = re.compile(rf"""
    {_QUOTE} term {_QUOTE} \s* : \s* {_QUOTE} (\w+) {_QUOTE}
    | {_QUOTE} term {_QUOTE} \s* : \s*  \{{ {_QUOTE} IN {_QUOTE} ( [^}}]+ )
    """, FLAGS)

ABBREVS = """Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec """

CONVERT = {
    'cm': 10.0,
    'dm': 100.0,
    'm': 1000.0,
    'mm': 1.0,
    'µm': 1.0e-3,
}


def convert(number, units):
    """Normalize the units to meters."""
    return number * CONVERT.get(units, 1.0)
