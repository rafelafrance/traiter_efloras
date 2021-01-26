"""Common descriptors snippets, plant-wide traits (words or phrases)."""

import spacy

from traiter.pipes.entity_data import RejectMatch
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
def descriptor(ent):
    """Enrich a phrase match."""
    label = _DESCRIPTORS_DICT.get(ent[0]._.label_cache)
    value = ent.text.lower()

    if value not in _IS_DESCRIPTOR:
        raise RejectMatch
    print(f'descriptor {ent}')
    print(label)

    ent._.new_label = label
    ent._.data = {label: REPLACE.get(value, value)}
