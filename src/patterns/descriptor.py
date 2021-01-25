"""Common descriptors snippets, plant-wide traits (words or phrases)."""

import spacy

from ..pylib.consts import REPLACE, TERMS

_DESCRIPTORS_DICT = {t['label']: t['label'] for t in TERMS
                     if t.get('category') == 'descriptor'}
_DESCRIPTORS_DICT['sex'] = 'reproduction'
_IS_DESCRIPTOR = {t['pattern'] for t in TERMS if t.get('category') == 'descriptor'}

DESCRIPTOR_LABELS = sorted(_DESCRIPTORS_DICT.values())

DESCRIPTOR = [
    {
        'label': 'descriptor',
        'on_match': 'descriptor.v1',
        'patterns': [[
            {'ENT_TYPE': {'IN': list(_DESCRIPTORS_DICT.keys())}},
        ]],
    },
]


@spacy.registry.misc(DESCRIPTOR[0]['on_match'])
def descriptor(span):
    """Enrich a phrase match."""
    label = _DESCRIPTORS_DICT[span[0].ent_type_]
    value = span.lower_

    if value not in _IS_DESCRIPTOR:
        return

    data = dict(_label=label)
    data[label] = REPLACE.get(value, value)

    return data
