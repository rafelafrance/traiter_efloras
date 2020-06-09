"""Common descriptors snippets, plant-wide traits (words or phrases)."""

from ..pylib.terms import TERMS

DESCRIPTORS_DICT = {t['label']: t['label'] for t in TERMS
                    if t['category'] == 'descriptor'}
DESCRIPTORS_DICT['sex'] = 'reproduction'

DESCRIPTOR_LABELS = sorted(DESCRIPTORS_DICT.values())

IS_DESCRIPTOR = {t['pattern'] for t in TERMS if t['category'] == 'descriptor'}


def descriptor(span):
    """Enrich a phrase match."""
    label = DESCRIPTORS_DICT[span[0]._.label]
    value = span.lower_

    if value not in IS_DESCRIPTOR:
        return {}

    return dict(
        value=value,
        relabel=label,
        start=span.start_char,
        end=span.end_char,
    )


DESCRIPTOR = {
    'name': 'descriptor',
    'matchers': [
        {
            'label': 'descriptor',
            'on_match': descriptor,
            'patterns': [[
                {'_': {'label': {'IN': list(DESCRIPTORS_DICT.keys())}}},
            ]],
        },
    ]
}
