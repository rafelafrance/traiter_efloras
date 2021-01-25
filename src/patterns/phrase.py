"""Match unadorned phrases attached to a plant part."""

import spacy
from traiter.consts import COMMA

from ..pylib.consts import REPLACE, TERMS

LITERAL_LABELS = {t['label'] for t in TERMS if t.get('category') == 'literal'}
LITERAL_LABELS = sorted(LITERAL_LABELS)

PHRASE = [
    {
        'label': 'phrase',
        'on_match': 'phrase.v1',
        'patterns': [
            [
                {'ENT_TYPE': {'IN': LITERAL_LABELS}},
            ],
            [
                {'LOWER': {'IN': ['without']}},
                {'POS': {'IN': ['ADJ']}, 'OP': '?'},
                {'TEXT': {'IN': COMMA}, 'OP': '?'},
                {'ENT_TYPE': {'IN': LITERAL_LABELS}},
            ],
        ],
    },
]


@spacy.registry.misc(PHRASE[0]['on_match'])
def phrase(span):
    """Enrich the match."""
    data = {}
    negate = ''
    for token in span:
        label = token.ent_type_
        value = token.lower_
        if value == 'without':
            negate = 'not '
        elif label in LITERAL_LABELS:
            value = REPLACE.get(value, value)
            data = {'_label': label, label: negate + value}
    return data
