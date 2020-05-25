"""Common color snippets."""

from ..pylib.terms import TERMS


CATEGORIES = {t['pattern']: t['category'] for t in TERMS
              if t['label'] == 'descriptor'}


def descriptor(span):
    """Enrich a phrase match."""
    value = span.text.lower()
    category = CATEGORIES.get(value, '')
    return dict(
        value=value,
        category=category,
        start=span.start_char,
        end=span.end_char,
    )


PLANT_DESCRIPTOR = {
    'name': 'descriptor',
    'matchers': [
        {
            'label': 'descriptor',
            'on_match': descriptor,
            'patterns': [[{'_': {'label': 'descriptor'}}]],
        },
    ]
}
