"""Common color snippets."""

from ..pylib.terms import TERMS

_DESCRIPTORS = {t['label']: t['label'] for t in TERMS
                if t['category'] == 'descriptor'}
_DESCRIPTORS['sex'] = 'reproduction'

DESCRIPTOR_LABELS = sorted(_DESCRIPTORS.values())
_LABELS = list(_DESCRIPTORS.keys())

_IS_DESCRIPTOR = {t['pattern'] for t in TERMS if t['category'] == 'descriptor'}


def descriptor(span):
    """Enrich a phrase match."""
    label = _DESCRIPTORS[span[0]._.label]
    value = span.lower_

    if value not in _IS_DESCRIPTOR:
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
                {'_': {'label': {'IN': _LABELS}}},
            ]],
        },
    ]
}
