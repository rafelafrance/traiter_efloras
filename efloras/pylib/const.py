"""Project-wide constants."""

from pathlib import Path

from traiter.const import CLOSE, COMMA, DASH, FLOAT_TOKEN_RE, OPEN, SLASH
from traiter.terms.csv_ import Csv

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('floras') > -1 else Path.cwd().parent

DATA_DIR = BASE_DIR / 'data'

EFLORAS_DIR = DATA_DIR / 'eFloras'
EFLORAS_FAMILIES = DATA_DIR / 'efloras_families' / 'eFloras_family_list.csv'

# #########################################################################
# Term related constants
TERM_PATH = BASE_DIR / 'efloras' / 'vocabulary' / 'terms.csv'
TERMS = Csv.shared('colors units')
TERMS += Csv.read_csv(TERM_PATH)
TERMS += Csv.hyphenate_terms(TERMS)
TERMS += Csv.trailing_dash(TERMS, label='color')
TERMS.drop('imperial_length')

REPLACE = TERMS.pattern_dict('replace')
REMOVE = TERMS.pattern_dict('remove')

TRAITS = set(""" color color_mod count location margin_shape part
    size shape sex subpart woodiness """.split())


# #########################################################################
# Tokenizer constants
ABBREVS = """
    Jan. Feb. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
    ca. """.split()

# #########################################################################
# Pattern related constants
CONJ = ['or', 'and']
TO = ['to']
MISSING = """ without missing lack lacking except excepting not rarely """.split()

COMMON_PATTERNS = {
    '(': {'TEXT': {'IN': OPEN}},
    ')': {'TEXT': {'IN': CLOSE}},
    '-': {'TEXT': {'IN': DASH}, 'OP': '+'},
    '-*': {'TEXT': {'IN': DASH}, 'OP': '*'},
    '/': {'TEXT': {'IN': SLASH}},
    ',': {'TEXT': {'IN': COMMA}},
    'to': {'LOWER': {'IN': TO}},
    '-/or': {'LOWER': {'IN': DASH + TO + CONJ}, 'OP': '+'},
    '-/to': {'LOWER': {'IN': DASH + TO}, 'OP': '+'},
    'and/or': {'LOWER': {'IN': CONJ}},
    'missing': {'LOWER': {'IN': MISSING}},
    '9': {'IS_DIGIT': True},
    '99.9': {'TEXT': {'REGEX': FLOAT_TOKEN_RE}},
    '99-99': {'ENT_TYPE': {'REGEX': '^range'}},
    '99.9-99.9': {'ENT_TYPE': {'REGEX': '^range'}},
}
