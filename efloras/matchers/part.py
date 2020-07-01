"""Plant part parser."""

import re

from traiter.util import FLAGS  # pylint: disable=import-error

from .shared import PER_COUNT, PER_COUNTS
from ..pylib.terms import REPLACE, TERMS
from ..pylib.util import TRAIT_STEP

_PATTERNS = [t for t in TERMS if t['label'] == 'part']
_PATTERNS = sorted([t['pattern'] for t in _PATTERNS], key=len, reverse=True)

PATTERN_RE = '|'.join(_PATTERNS)
PATTERN_RE = re.compile(f'({PATTERN_RE})', FLAGS)

_SEX = {t['pattern']: t['replace'] for t in TERMS if t['label'] in ('sex',)}


def part(span):
    """Enrich a plant part match."""
    data = {}

    for token in span:
        label = token.ent_type_
        value = token.lower_
        if label == 'part':
            data['part'] = REPLACE.get(value, value)
        elif label == 'sex':
            data['sex'] = _SEX[value]
        elif label == 'location':
            data['location'] = value
        elif token.lower_ in PER_COUNT:
            data['group'] = REPLACE.get(token.lower_, token.lower_)

    return data


PART = {
    'name': 'part',
    TRAIT_STEP: [
        {
            'label': 'part',
            'on_match': part,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': ['sex', 'location']}, 'OP': '*'},
                    {'ENT_TYPE': 'part'},
                ],
                [
                    {'ENT_TYPE': 'location'},
                    {'LOWER': {'IN': PER_COUNTS}, 'OP': '?'},
                    {},
                    {'ENT_TYPE': 'part'},
                ],
                [
                    {'ENT_TYPE': 'location'},
                    {'LOWER': {'IN': PER_COUNTS}, 'OP': '?'},
                    {'ENT_TYPE': 'part'},
                ],
            ],
        },
    ],
}
