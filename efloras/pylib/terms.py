"""Setup terms."""

# pylint: disable=superfluous-parens

import csv
import re

from hyphenate import hyphenate_word
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


def hyphenate_terms(terms):
    """Systematically handle hyphenated terms."""
    new_terms = []
    for term in terms:
        if term['hyphenate']:
            parts = term['hyphenate'].split()
        else:
            parts = hyphenate_word(term['pattern'])
        for i in range(1, len(parts)):
            replace = term['replace']
            hyphenated = ''.join(parts[:i]) + '-' + ''.join(parts[i:])
            new_terms.append({
                'label': term['label'],
                'pattern': hyphenated,
                'attr': term['attr'],
                'replace': replace if replace else term['pattern'],
                'category': term['category'],
            })
            hyphenated = ''.join(parts[:i]) + '\xad' + ''.join(parts[i:])
            new_terms.append({
                'label': term['label'],
                'pattern': hyphenated,
                'attr': term['attr'],
                'replace': replace if replace else term['pattern'],
                'category': term['category'],
            })
    return new_terms


TERMS = read_terms()
TERMS += hyphenate_terms(TERMS)

LABELS = sorted({t['label'] for t in TERMS})
REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}
CATEGORY = {t['pattern']: c for t in TERMS if (c := t.get('category'))}

PATTERN_RE = re.compile(rf"""
    {QUOTE} term {QUOTE} \s* : \s* {QUOTE} (\w+) {QUOTE}
    | {QUOTE} term {QUOTE} \s* : \s*  \{{ {QUOTE} IN {QUOTE} ( [^}}]+ )
    """, FLAGS)
