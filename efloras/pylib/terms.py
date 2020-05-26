"""Setup terms."""

import csv
import json

import re
from traiter.util import FLAGS  # pylint: disable=import-error

import efloras.pylib.family_util as futil

TERM_PATH = futil.DATA_DIR / 'terms.csv'

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


def terms_from_patterns(patterns):
    """Get all of the terms required by the matchers."""
    string = json.dumps(patterns)
    terms = set()
    for match in PATTERN_RE.finditer(string):
        if match.group(1):
            terms.add(match.group(1))
        else:
            terms |= {t for t in re.split(r'\W+', match.group(2)) if t}
    return [t for t in TERMS if t['label'] in terms]
