"""Plant subpart parser."""

from .consts import REPLACE, TERMS, TRAIT_STEP

_SEX = {t['pattern']: t['replace'] for t in TERMS if t['label'] in ('sex',)}


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


SUBPART = {
    TRAIT_STEP: [
        {
            'label': 'subpart',
            'on_match': subpart,
            'patterns': [[
                {'ENT_TYPE': {'IN': ['sex', 'location']}, 'OP': '*'},
                {'ENT_TYPE': 'subpart'},
            ]],
        },
    ],
}
