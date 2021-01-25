"""Plant subpart parser."""

import spacy

from ..pylib.consts import REPLACE, TERMS

_SEX = {t['pattern']: t['replace'] for t in TERMS if t['label'] in ('sex',)}

SUBPART = [
    {
        'label': 'subpart',
        'on_match': 'subpart.v1',
        'patterns': [[
            {'ENT_TYPE': {'IN': ['sex', 'location']}, 'OP': '*'},
            {'ENT_TYPE': 'subpart'},
        ]],
    },
]


@spacy.registry.misc(SUBPART[0]['on_match'])
def subpart(span):
    """Enrich a plant subpart match."""
    data = {}

    for token in span:
        label = token.ent_type_
        value = token.lower_
        if label == 'subpart':
            data['subpart'] = REPLACE.get(value, value)
        elif label == 'sex':
            data['sex'] = _SEX[value]
        elif label == 'location':
            data['location'] = value

    return data
