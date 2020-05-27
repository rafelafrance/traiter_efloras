"""Plant part parser."""

import re

from traiter.util import FLAGS  # pylint: disable=import-error

from ..pylib.terms import TERMS

PARTS = [t for t in TERMS if t['label'] == 'plant_part']

REPLACES = {t['pattern']: t['replace'] for t in PARTS}

PATTERNS = sorted([t['pattern'] for t in PARTS], key=len, reverse=True)

PATTERN_RE = '|'.join(PATTERNS)
PATTERN_RE = re.compile(f'({PATTERN_RE})', FLAGS)

KEYS = set(PATTERNS)

SEX = {t['pattern']: t['replace'] for t in TERMS
       if t['label'] in ('plant_sex', 'plant_sex2')}


def part(span):
    """Enrich a plant part match."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label
        value = token.text.lower()
        if label == 'plant_part':
            data['value'] = REPLACES.get(value, '')
        elif label == 'plant_sex':
            data['sex'] = SEX[value]
        elif label == 'part_location':
            data['location'] = value

    return data


PLANT_PART = {
    'name': 'part',
    'matchers': [
        {
            'label': 'part',
            'on_match': part,
            'patterns': [[
                {'_': {'label': {'IN': [
                    'plant_sex', 'part_location']}}, 'OP': '*'},
                {'_': {'label': 'plant_part'}}
            ]],
        },
    ],
}
