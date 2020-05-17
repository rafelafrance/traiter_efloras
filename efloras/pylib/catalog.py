"""Setup terms."""

import csv

import efloras.pylib.util as util

TERM_PATH = util.DATA_DIR / 'terms.csv'

DASH = '–-'


def read_terms():
    """Read and cache the terms."""
    with open(TERM_PATH) as term_file:
        reader = csv.DictReader(term_file)
        return [t for t in reader]


TERMS = read_terms()
REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}
