"""Plant part parser."""

import regex
from traiter.util import FLAGS  # pylint: disable=import-error

from ..pylib.terms import TERMS


PARTS = [t for t in TERMS if t['label'] == 'plant_part']

CATEGORIES = {t['pattern']: t['category'] for t in PARTS}

PATTERNS = sorted([t['pattern'] for t in PARTS], key=len, reverse=True)

SPLITTER = '|'.join(PATTERNS)
SPLITTER = regex.compile(f'({SPLITTER})', FLAGS)

KEYS = set(PATTERNS)

SEX = {t['pattern']: t['category'] for t in TERMS
       if t['label'] == 'plant_sex'}
SEX_RE = '|'.join(SEX)
SEX_RE = regex.compile(fr' \b ({SEX_RE}) \b', FLAGS)


def part(span):
    """Enrich a plant part match."""
    value = span.text.lower()
    value = CATEGORIES.get(value, '')
    trait = dict(
        value=value,
        start=span.start_char,
        end=span.end_char,
    )
    if match := SEX_RE.search(span.text):
        trait['sex'] = SEX[match.group().lower()]
    return trait


PLANT_PART = {
    'name': 'part',
    'trait_names': ['plant_part'],
    'matchers': [
        {
            'label': 'part',
            'on_match': part,
            'patterns': [[{'_': {'label': 'plant_part'}}]],
        },
    ],
}
