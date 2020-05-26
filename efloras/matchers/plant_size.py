"""Common color snippets."""

import re

from traiter.util import to_positive_float  # pylint: disable=import-error

from .shared import RANGE_GROUPS
from ..pylib.terms import TERMS

# Normalize dimension notations
DIMENSIONS = {t['pattern']: t['category'] for t in TERMS
              if t['label'] == 'dimension'}

# Normalize unit notations
UNITS = {t['pattern']: t['category'] for t in TERMS
         if t['label'] == 'length_units'}

# Multiply units by this to normalize to millimeters
MULTIPLY = {t['category']: to_positive_float(m) for t in TERMS
            if t['label'] == 'length_units' if (m := t['replace'])}


def size(span):
    """Enrich a phrase match."""
    dims = scan_tokens(span)
    dims = fix_dimensions(dims)
    data = fill_data(span, dims)
    return data


def fill_data(span, dims):
    """Move fields into correct place & give them consistent names."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    value = {}

    for dim in dims:
        dim_name = dim['dim_name']

        # Rename value fields & multiply values to put into millimeters
        for field in """ min low high max """.split():
            if datum := dim.get(field):
                key = f'{dim_name}_{field}'
                value[key] = round(datum * dim['times'], 3)

        # Rename the unit fields
        if datum := dim.get('units'):
            key = f'{dim_name}_units'
            value[key] = datum.lower()

        # Get the sex field if it's there
        if datum := dim.get('sex'):
            value['sex'] = re.sub(r'\W+', '', datum.lower())

    data['value'] = value

    return data


def fix_dimensions(dims):
    """Handle width comes before length and one of them is missing units."""
    if len(dims) > 1:
        # Length & width are reversed
        if (dims[0].get('dimension') == 'width'
                or dims[1].get('dimension') == 'length'):
            dims[0], dims[1] = dims[1], dims[0]
        # Missing units in the length (most likely)
        if not dims[0].get('times'):
            dims[0]['times'] = dims[1]['times']
        # Missing units in the width
        if not dims[1].get('times'):
            dims[1]['times'] = dims[0]['times']

    dims[0]['dim_name'] = dims[0].get('dimension', 'length')
    if len(dims) > 1:
        dims[1]['dim_name'] = dims[1].get('dimension', 'width')

    return dims


def scan_tokens(span):
    """Scan tokens for the various fields."""
    dims = [{}]
    idx = 0

    for token in span:
        label = token._.label

        # Convert the size fields to floats
        if label in """ min low high max """.split():
            dims[idx][label] = to_positive_float(token.text)

        # Save the units and get the unit multiplier
        elif label == 'length_units':
            units = UNITS[token.text.lower()]
            dims[idx]['units'] = units
            dims[idx]['times'] = MULTIPLY[units]

        elif label == 'dimension':
            dims[idx]['dimension'] = DIMENSIONS[token.text.lower()]

        elif label in ('sex_enclosed', 'plant_sex'):
            value = token.text.lower()
            value = re.sub(r'\W+', '', value)
            dims[idx]['sex'] = value

        elif label == 'cross':
            idx += 1
            dims.append({})

    return dims


PLANT_SIZE = {
    'name': 'size',
    'groupers': {
        **RANGE_GROUPS,
        'sex_enclosed': [[
            {'_': {'label': 'open'}},
            {'_': {'label': 'plant_sex'}},
            {'_': {'label': 'close'}},
        ]],
    },
    'matchers': [
        {
            'label': 'size',
            'on_match': size,
            'patterns': [
                [
                    {'_': {'label': 'min'}, 'OP': '?'},
                    {'_': {'label': 'low'}},
                    {'_': {'label': 'high'}, 'OP': '?'},
                    {'_': {'label': 'max'}, 'OP': '?'},
                    {'_': {'label': 'length_units'}},
                    {'_': {'label': {
                        'IN': ['dimension', 'sex_enclosed', 'plant_sex']}},
                        'OP': '*'},
                ], [
                    {'_': {'label': 'high'}},
                    {'_': {'label': 'length_units'}},
                    {'_': {'label': {
                        'IN': ['dimension', 'sex_enclosed', 'plant_sex']}},
                        'OP': '*'},
                ],
                [
                    {'_': {'label': 'min'}, 'OP': '?'},
                    {'_': {'label': 'low'}},
                    {'_': {'label': 'high'}, 'OP': '?'},
                    {'_': {'label': 'max'}, 'OP': '?'},
                    {'_': {'label': 'length_units'}, 'OP': '?'},
                    {'_': {'label': {
                        'IN': ['dimension', 'sex_enclosed', 'plant_sex']}},
                        'OP': '*'},
                    {'_': {'label': 'cross'}},
                    {'_': {'label': 'min'}, 'OP': '?'},
                    {'_': {'label': 'low'}},
                    {'_': {'label': 'high'}, 'OP': '?'},
                    {'_': {'label': 'max'}, 'OP': '?'},
                    {'_': {'label': 'length_units'}},
                    {'_': {'label': {
                        'IN': ['dimension', 'sex_enclosed', 'plant_sex']}},
                        'OP': '*'},
                ],
            ],
        },
    ]
}
