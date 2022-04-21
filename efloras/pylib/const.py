"""Project-wide constants."""
import os
import re
from pathlib import Path

from traiter.const import CLOSE, COMMA, CROSS, DASH, FLOAT_TOKEN_RE, OPEN, PLUS, SLASH
from traiter.terms.db import Db

# Download site
SITE = 'http://www.efloras.org'

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('floras') > -1 else Path.cwd().parent

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"
MOCK_DIR = ROOT_DIR / "tests" / "mock_data"

EFLORAS_DIR = DATA_DIR / 'eFloras'
EFLORAS_FAMILIES = DATA_DIR / 'efloras_families' / 'eFloras_family_list.csv'

TERM_DB = DATA_DIR / "plant_terms.sqlite"
if not TERM_DB.exists():
    TERM_DB = MOCK_DIR / "plant_terms.sqlite"

# #########################################################################
# Term related constants
TERMS = Db.shared('colors units')
TERMS += Db.select_term_set(TERM_DB, "plant_treatment")
TERMS += Db.hyphenate_terms(TERMS)
TERMS += Db.trailing_dash(TERMS, label='color')
TERMS.drop('imperial_length')

REPLACE = TERMS.pattern_dict('replace')
REMOVE = TERMS.pattern_dict('remove')

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
# Common patterns for parsing
CONJ = ['or', 'and']
TO = ['to']
MISSING = """ without missing lack lacking except excepting not rarely """.split()

COMMON_PATTERNS = {
    '(': {'TEXT': {'IN': OPEN}},
    ')': {'TEXT': {'IN': CLOSE}},
    '-': {'TEXT': {'IN': DASH}, 'OP': '+'},
    '-*': {'TEXT': {'IN': DASH}, 'OP': '*'},
    '[+]': {'TEXT': {'IN': PLUS}},
    '/': {'TEXT': {'IN': SLASH}},
    ',': {'TEXT': {'IN': COMMA}},
    'x': {'TEXT': {'IN': CROSS}},
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
# Entities

TRAITS = set(""" color color_mod count location margin_shape part
    size shape sex subpart woodiness part_as_loc """.split())

FORGET = """ about cross color_mod dim dimension imperial_length imperial_mass
    margin_leader metric_length metric_mass not_a_range per_count
    quest shape_leader shape_suffix surface units
    range.low range.min.low range.low.high range.low.max range.min.low.high
    range.min.low.max range.low.high.max range.min.low.high.max
    """.split()
