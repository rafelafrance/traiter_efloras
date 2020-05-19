"""Plant part parser."""

from traiter.util import DotDict as Trait

from ..pylib.terms import TERMS

CATEGORIES = {t['pattern']: c for t in TERMS if (c := t['category'])}


def part(span):
    """Enrich a plant part match."""
    return Trait(
        value=CATEGORIES.get(span.text.lower()),
        start=span.start_char,
        end=span.end_char,
        raw_value=span.text,
    )


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
