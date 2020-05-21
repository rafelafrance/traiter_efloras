"""Common color snippets."""

import regex
from traiter.util import to_positive_float

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
        raw_value=span.text,
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
            value['sex'] = datum.lower()

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
        term = token._.term

        # Convert the size fields to floats
        if term in 'min_size low_size high_size max_size'.split():
            key = term.split('_')[0]  # Remove "_size"
            dims[idx][key] = to_positive_float(token.text)

        # Save the units and get the unit multiplier
        elif term == 'length_units':
            units = UNITS[token.text.lower()]
            dims[idx]['units'] = units
            dims[idx]['times'] = MULTIPLY[units]

        elif term == 'dimension':
            dims[idx]['dimension'] = DIMENSIONS[token.text.lower()]

        elif term == 'sex':
            value = token.text.lower()
            value = regex.sub(r'\W+', '', value)
            dims[idx]['sex'] = value

        elif term == 'cross':
            idx += 1
            dims.append({})

    return dims


PLANT_SIZE = {
    'name': 'size',
    'trait_names': """ calyx_size corolla_size flower_size hypanthium_size
        leaf_size petal_size petiole_size seed_size sepal_size """.split(),
    'groupers': {
        'min_size': [[
            {'_': {'term': 'open'}},
            {'_': {'term': 'float'}},
            {'_': {'term': {'IN': ['dash', 'prep']}}},
            {'_': {'term': 'close'}},
        ]],
        'low_size': [[
            {'_': {'term': 'float'}},
        ]],
        'high_size': [[
            {'_': {'term': {'IN': ['dash', 'prep']}}},
            {'_': {'term': 'float'}},
        ]],
        'max_size': [[
            {'_': {'term': 'open'}},
            {'_': {'term': {'IN': ['dash', 'prep']}}},
            {'_': {'term': 'float'}},
            {'_': {'term': 'close'}},
        ]],
        'sex': [[
            {'_': {'term': 'open'}, 'OP': '?'},
            {'_': {'term': 'plant_sex'}},
            {'_': {'term': 'close'}, 'OP': '?'},
        ]],
    },
    'matchers': [
        {
            'label': 'size',
            'on_match': size,
            'patterns': [
                [
                    {'_': {'term': 'min_size'}, 'OP': '?'},
                    {'_': {'term': 'low_size'}},
                    {'_': {'term': 'high_size'}, 'OP': '?'},
                    {'_': {'term': 'max_size'}, 'OP': '?'},
                    {'_': {'term': 'length_units'}},
                    {'_': {'term': 'dimension'}, 'OP': '?'},
                    {'_': {'term': 'sex'}, 'OP': '?'},
                ], [
                    {'_': {'term': 'high_size'}},
                    {'_': {'term': 'length_units'}},
                    {'_': {'term': 'dimension'}, 'OP': '?'},
                    {'_': {'term': 'sex'}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'size',
            'on_match': size,   # cross
            'patterns': [[
                {'_': {'term': 'min_size'}, 'OP': '?'},
                {'_': {'term': 'low_size'}},
                {'_': {'term': 'high_size'}, 'OP': '?'},
                {'_': {'term': 'max_size'}, 'OP': '?'},
                {'_': {'term': 'length_units'}, 'OP': '?'},
                {'_': {'term': 'dimension'}, 'OP': '?'},
                {'_': {'term': 'cross'}},
                {'_': {'term': 'min_size'}, 'OP': '?'},
                {'_': {'term': 'low_size'}},
                {'_': {'term': 'high_size'}, 'OP': '?'},
                {'_': {'term': 'max_size'}, 'OP': '?'},
                {'_': {'term': 'length_units'}},
                {'_': {'term': 'dimension'}, 'OP': '?'},
                {'_': {'term': 'sex'}, 'OP': '?'},
            ]],
        },
    ]
}
