"""Setup terms."""

import csv
import json

import regex
import traiter.util as t_util

import efloras.pylib.util as util

TERM_PATH = util.DATA_DIR / 'terms.csv'

DASH = '–-'
QUOTE = """["']"""


def read_terms():
    """Read and cache the terms."""
    with open(TERM_PATH) as term_file:
        reader = csv.DictReader(term_file)
        return [t for t in reader]


TERMS = read_terms()
REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}


PATTERN_RE = regex.compile(rf"""
    {QUOTE}term{QUOTE} \s* :\s* {QUOTE} (?P<term> \w+ ) {QUOTE}
    """, t_util.FLAGS)


def terms_from_patterns(patterns):
    """Get all of the terms required by the matchers."""
    patterns = [p['patterns'] for p in patterns.values()]
    string = json.dumps(patterns)
    terms = set()
    for match in PATTERN_RE.finditer(string):
        terms.add(match.group('term'))
    return [t for t in TERMS if t['label'] in terms]
