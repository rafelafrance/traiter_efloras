"""Setup terms."""

# pylint: disable=superfluous-parens, import-error

import re

from traiter.pylib.terms import hyphenate_terms, read_terms
from traiter.pylib.util import FLAGS

from .util import VOCAB_DIR

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
