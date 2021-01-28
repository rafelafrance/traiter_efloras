"""Project-wide constants."""

from pathlib import Path

from traiter.terms.csv_ import Csv

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('floras') > -1 else Path.cwd().parent

DATA_DIR = BASE_DIR / 'data'

EFLORAS_DIR = DATA_DIR / 'eFloras'
EFLORAS_FAMILIES = DATA_DIR / 'efloras_families' / 'eFloras_family_list.csv'

TERM_PATH = BASE_DIR / 'src' / 'vocabulary' / 'terms.csv'
TERMS = Csv.shared('colors units')
TERMS += Csv.read_csv(TERM_PATH)
TERMS += Csv.hyphenate_terms(TERMS)
TERMS += Csv.trailing_dash(TERMS, label='color')
TERMS.drop('imperial_length')

REPLACE = TERMS.pattern_dict('replace')
CATEGORY = TERMS.pattern_dict('category')
REMOVE = TERMS.pattern_dict('remove')

ABBREVS = """Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec ca """

MISSING = """ without missing lack lacking except excepting not rarely """.split()

IS_RANGE = {'REGEX': '^range'}
