"""Match unadorned phrases attached to a plant part."""

from .consts import COMMA, REPLACE, TERMS, TRAIT_STEP

_LITERAL_LABELS = {t['label'] for t in TERMS if t['category'] == 'literal'}
_LITERAL_LABELS = sorted(_LITERAL_LABELS)


def phrase(span):
    """Enrich the match."""
    data = {}
    negate = ''
    for token in span:
        label = token.ent_type_
        value = token.lower_
        if value == 'without':
            negate = 'not '
        elif label in _LITERAL_LABELS:
            value = REPLACE.get(value, value)
            data = {'_relabel': label, label: negate + value}
    return data


PHRASE = {
    TRAIT_STEP: [
        {
            'label': 'phrase',
            'on_match': phrase,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': _LITERAL_LABELS}},
                ],
                [
                    {'LOWER': {'IN': ['without']}},
                    {'POS': {'IN': ['ADJ']}, 'OP': '?'},
                    {'TEXT': {'IN': COMMA}, 'OP': '?'},
                    {'ENT_TYPE': {'IN': _LITERAL_LABELS}},
                ],
            ],
        },
    ]
}
