"""Setup terms."""

# pylint: disable=superfluous-parens

import csv
import re

from traiter.util import FLAGS  # pylint: disable=import-error

from .util import VOCAB_DIR

TERM_PATH = VOCAB_DIR / 'terms.csv'

DASH = '–-'
QUOTE = """["']"""


def read_terms():
    """Read and cache the terms."""
    with open(TERM_PATH) as term_file:
        reader = csv.DictReader(term_file)
        return list(reader)


TERMS = read_terms()
LABELS = sorted({t['label'] for t in TERMS})
REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}

PATTERN_RE = re.compile(rf"""
    {QUOTE} term {QUOTE} \s* : \s* {QUOTE} (\w+) {QUOTE}
    | {QUOTE} term {QUOTE} \s* : \s*  \{{ {QUOTE} IN {QUOTE} ( [^}}]+ )
    """, FLAGS)
