"""Plant part parser."""

import re

from traiter.util import FLAGS  # pylint: disable=import-error

from ..pylib.terms import REPLACE, TERMS

_PATTERNS = [t for t in TERMS if t['label'] == 'plant_part']
_PATTERNS = sorted([t['pattern'] for t in _PATTERNS], key=len, reverse=True)

PATTERN_RE = '|'.join(_PATTERNS)
PATTERN_RE = re.compile(f'({PATTERN_RE})', FLAGS)

_SEX = {t['pattern']: t['replace'] for t in TERMS
        if t['label'] in ('sex', 'plant_sex2')}


def part(span):
    """Enrich a plant part match."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label
        value = token.lower_
        if label == 'plant_part':
            data['value'] = REPLACE.get(value, value)
        elif label == 'sex':
            data['sex'] = _SEX[value]
        elif label == 'location':
            data['location'] = value

    return data


PART = {
    'name': 'part',
    'matchers': [
        {
            'label': 'part',
            'on_match': part,
            'patterns': [[
                {'_': {'label': {'IN': ['sex', 'location']}}, 'OP': '*'},
                {'_': {'label': 'plant_part'}}
            ]],
        },
    ],
}
