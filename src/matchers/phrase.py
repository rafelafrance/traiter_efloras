"""Match unadorned phrases attached to a plant part."""

from ..pylib.terms import REPLACE, TERMS
from ..pylib.util import TRAIT_STEP

LITERAL_LABELS = {t['label'] for t in TERMS if t['category'] == 'literal'}
LITERAL_LABELS = sorted(LITERAL_LABELS)


def phrase(span):
    """Enrich the match."""
    label = span[0].ent_type_
    value = span.lower_

    data = dict(_relabel=label)
    data[label] = REPLACE.get(value, value)

    return data


PHRASE = {
    'name': 'phrase',
    TRAIT_STEP: [
        {
            'label': 'phrase',
            'on_match': phrase,
            'patterns': [[
                {'ENT_TYPE': {'IN': LITERAL_LABELS}},
            ]],
        },
    ]
}
