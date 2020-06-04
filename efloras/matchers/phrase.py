"""Match unadorned phrases attached to a plant part."""

from ..pylib.terms import REPLACE


def phrase(span):
    """Enrich the match."""
    value = span.lower_

    return dict(
        value=REPLACE.get(value, value),
        # relabel=CATEGORY.get(value),
        start=span.start_char,
        end=span.end_char,
    )


PHRASE = {
    'name': 'phrase',
    'matchers': [
        {
            'label': 'phrase',
            'on_match': phrase,
            'patterns': [[
                {'_': {'label': 'habit'}},
            ]],
        },
    ]
}
