"""Project-wide constants."""

import re
from pathlib import Path

from traiter.const import CLOSE, COMMA, DASH, FLOAT_TOKEN_RE, OPEN, SLASH
from traiter.terms.csv_ import Csv

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('floras') > -1 else Path.cwd().parent

DATA_DIR = BASE_DIR / 'data'
PROCESSED_DATA = DATA_DIR / 'processed'

EFLORAS_DIR = DATA_DIR / 'eFloras'
EFLORAS_FAMILIES = DATA_DIR / 'efloras_families' / 'eFloras_family_list.csv'

# Download site
SITE = 'http://www.efloras.org'

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
# Used to filter paragraphs in the source documents.
PARA_RE = [t['pattern'] for t in TERMS.with_label('part')]
PARA_RE = '|'.join(PARA_RE)
PARA_RE = re.compile(PARA_RE)

# #########################################################################
# Tokenizer constants
ABBREVS = """
    Jan. Feb. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
    ca. al. """.split()

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

# #########################################################################
# Remove these stray entities
FORGET = """ about color_mod dimension imperial_length imperial_mass
    margin_leader metric_length metric_mass not_a_range per_count quest
    shape_leader shape_suffix surface
    range.low range.min.low range.low.high range.low.max range.min.low.high
    range.min.low.max range.low.high.max range.min.low.high.max
    """.split()
