"""Utilities for working with terms."""
import csv
from collections import defaultdict
import efloras.pylib.util as util


def all_terms():
    """Read terms."""
    terms = defaultdict(lambda: defaultdict(list))
    with open(util.DATA_DIR / 'terms.csv') as term_file:
        reader = csv.DictReader(term_file)
        for row in reader:
            terms[row['matcher']][row['type']].append(row)
    return terms


TERMS = all_terms()


def replacements(name):
    """Get replacement values for the terms."""
    combined = {**TERMS[name], **TERMS['shared']}
    combined = util.flatten(list(combined.values()))
    return {t['term']: t['replace'] for t in combined if t['replace']}
