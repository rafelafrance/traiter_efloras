"""Common descriptors snippets, plant-wide traits (words or phrases)."""

from ..pylib.consts import REPLACE, TERMS, TRAIT_STEP

_DESCRIPTORS_DICT = {t['label']: t['label'] for t in TERMS
                     if t['category'] == 'descriptor'}
_DESCRIPTORS_DICT['sex'] = 'reproduction'
_IS_DESCRIPTOR = {t['pattern'] for t in TERMS if t['category'] == 'descriptor'}

DESCRIPTOR_LABELS = sorted(_DESCRIPTORS_DICT.values())


def descriptor(span):
    """Enrich a phrase match."""
    label = _DESCRIPTORS_DICT[span[0].ent_type_]
    value = span.lower_

    if value not in _IS_DESCRIPTOR:
        return {'_forget': True}

    data = dict(_label=label)
    data[label] = REPLACE.get(value, value)

    return data


DESCRIPTOR = {
    TRAIT_STEP: [
        {
            'label': 'descriptor',
            'on_match': descriptor,
            'patterns': [[
                {'ENT_TYPE': {'IN': list(_DESCRIPTORS_DICT.keys())}},
            ]],
        },
    ],
}
