"""Plant part parser."""

import regex
from traiter.util import FLAGS

from ..pylib.terms import TERMS

CATEGORIES = {t['pattern']: c for t in TERMS if (c := t['category'])}


def part(span):
    """Enrich a plant part match."""
    value = CATEGORIES.get(span.text.lower(), '')
    trait = dict(
        value=value,
        start=span.start_char,
        end=span.end_char,
        raw_value=span.text,
    )
    if match := regex.search(r' pistillate | staminate ', span.text, FLAGS):
        trait['sex'] = match.group().lower()
    return trait


PLANT_PART = {
    'name': 'part',
    'trait_names': ['plant_part'],
    'matchers': {
        'part': {
            'on_match': part,
            'patterns': [[{'_': {'term': 'plant_part'}}]],
        },
    }
}
