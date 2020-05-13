"""Build a catalog of terms."""

from traiter.catalog import Catalog

import efloras.pylib.util as util


# TODO: Delete these
OPEN = {'TEXT': {'REGEX': r'^[(\[]$'}}
CLOSE = {'TEXT': {'REGEX': r'^[)\]]$'}}
DASH = {'TEXT': {'REGEX': r'^[\–\-]$'}}
DASH_Q = {'TEXT': {'REGEX': r'^[\–\-]$'}, 'OP': '?'}
CROSS = {'TEXT': {'REGEX': r'^[x×]$'}}
FLOAT = {'LIKE_NUM': True}
INT = {'TEXT': {'REGEX': r'^\d+$'}}
STOP_PUNCT = {'TEXT': {'REGEX': r'^[;.]$'}}
SEP = {'TEXT': {'REGEX': r'^[;.,:]$'}}
DASH_LIKE = {'LOWER': {'IN': ['or', 'to']}}

CATALOG = Catalog()
CATALOG.read_terms(util.DATA_DIR / 'terms.csv')
