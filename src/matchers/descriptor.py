"""Common descriptors snippets, plant-wide traits (words or phrases)."""

from ..pylib.terms import REPLACE, TERMS
from ..pylib.util import TRAIT_STEP

DESCRIPTORS_DICT = {t['label']: t['label'] for t in TERMS
                    if t['category'] == 'descriptor'}
DESCRIPTORS_DICT['sex'] = 'reproduction'

DESCRIPTOR_LABELS = sorted(DESCRIPTORS_DICT.values())

IS_DESCRIPTOR = {t['pattern'] for t in TERMS if t['category'] == 'descriptor'}


def descriptor(span):
    """Enrich a phrase match."""
    label = DESCRIPTORS_DICT[span[0].ent_type_]
    value = span.lower_

    if value not in IS_DESCRIPTOR:
        return {'_skip': True}

    data = dict(_relabel=label)
    data[label] = REPLACE.get(value, value)

    return data


DESCRIPTOR = {
    TRAIT_STEP: [
        {
            'label': 'descriptor',
            'on_match': descriptor,
            'patterns': [[
                {'ENT_TYPE': {'IN': list(DESCRIPTORS_DICT.keys())}},
            ]],
        },
    ],
}
