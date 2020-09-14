"""Common size snippets."""

import re
from functools import partial

from .shared import CLOSE, CROSS, NUMBER, OPEN
from ..pylib.util import GROUP_STEP, REPLACE, TRAIT_STEP


def size(span, high_only=False):
    """Enrich a phrase match."""
    dims = scan_tokens(span, high_only)
    dims = fix_dimensions(dims)
    data = fill_data(dims)
    return data


def scan_tokens(span, high_only):
    """Scan tokens for the various fields."""
    dims = [{}]

    for token in span:
        label = token.ent_type_

        if label == 'range':
            for key, value in token._.data.items():
                dims[-1][key] = value
            if high_only:
                dims[-1]['high'] = dims[-1]['low']
                del dims[-1]['low']

        elif label == 'length_units':
            dims[-1]['units'] = REPLACE[token.lower_]

        elif label == 'dimension':
            dims[-1]['dimension'] = REPLACE[token.lower_]

        elif label in ('sex_enclosed', 'sex'):
            dims[-1]['sex'] = re.sub(r'\W+', '', token.lower_)

        elif label == 'quest':
            dims[-1]['uncertain'] = True

        elif token.lower_ in CROSS:
            dims.append({})

    return dims


def fix_dimensions(dims):
    """Handle width comes before length and one of them is missing units."""
    dim = ''
    if len(dims) == 1:
        dims[0]['dimension'] = dims[0].get('dimension', 'length')
    elif not dims[0].get('dimension') and (dim := dims[1].get('dimension')):
        dims[0]['dimension'] = 'length' if dim == 'width' else 'width'
    elif not dims[1].get('dimension') and (dim := dims[0].get('dimension')):
        dims[1]['dimension'] = 'length' if dim == 'width' else 'width'
    else:
        dims[0]['dimension'] = 'length'
        dims[1]['dimension'] = 'width'
        if len(dims) > 2:
            dims[2]['dimension'] = 'thickness'
    return dims


def fill_data(dims):
    """Move fields into correct place & give them consistent names."""
    data = {}

    for dim in dims:
        dimension = dim['dimension']

        for field in """ min low high max """.split():
            if datum := dim.get(field):
                key = f'{dimension}_{field}'
                data[key] = round(datum, 3)

        if datum := dim.get('units'):
            key = f'{dimension}_units'
            data[key] = datum.lower()

        if datum := dim.get('sex'):
            data['sex'] = datum

        if dim.get('uncertain'):
            data['uncertain'] = 'true'

    return data


def size_double_dim(span):
    """Handle the case when the dimensions are doubled but values are not.

    Like: Legumes 2.8-4.5 mm high and wide
    """
    data = size(span)
    dims = [REPLACE.get(t.lower_, t.lower_) for t in span
            if t.ent_type_ == 'dimension']

    new_data = {}
    for key, value in data.items():
        parts = key.split('_')
        if parts[0] in dims:
            parts[0] = dims[1] if parts[0] == dims[0] else dims[0]
            new_key = '_'.join(parts)
            new_data[new_key] = value

    return {**data, **new_data}


def not_a_size(_):
    """Flag this as a token to be deleted."""
    return {'_forget': True}


_FOLLOW = """ dimension sex_enclosed sex """.split()
_UNCERTAIN = """ quest quest_enclosed """.split()
_NOT_A_SIZE = """ for """.split()

SIZE = {
    GROUP_STEP: [
        {
            'label': 'sex_enclosed',
            'patterns': [[
                {'TEXT': {'IN': OPEN}},
                {'ENT_TYPE': 'sex'},
                {'TEXT': {'IN': CLOSE}},
            ]],
        },
    ],
    TRAIT_STEP: [
        {
            'label': 'size',
            'on_match': size,
            'patterns': [
                [
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units'},
                    {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                ],
                [
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units', 'OP': '?'},
                    {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                    {'LOWER': {'IN': CROSS}},
                    {'LOWER': 'to', 'OP': '?'},
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units'},
                    {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                ],
                [
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units', 'OP': '?'},
                    {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                    {'LOWER': {'IN': CROSS}},
                    {'LOWER': 'to', 'OP': '?'},
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units', 'OP': '?'},
                    {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                    {'LOWER': {'IN': CROSS}},
                    {'LOWER': 'to', 'OP': '?'},
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units'},
                    {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                ],
            ],
        },
        {
            'label': 'size',
            'on_match': partial(size, high_only=True),
            'patterns': [
                [
                    {'LOWER': 'to'},
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'LOWER': {'REGEX': NUMBER}},
                    {'ENT_TYPE': 'quest', 'OP': '?'},
                    {'ENT_TYPE': 'length_units'},
                    {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                ],
            ],
        },
        {
            'label': 'size',
            'on_match': size_double_dim,
            'patterns': [
                [
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units'},
                    {'ENT_TYPE': {'IN': 'sex_enclosed' 'sex'}, 'OP': '?'},
                    {'ENT_TYPE': 'dimension'},
                    {'LOWER': 'and'},
                    {'ENT_TYPE': 'dimension'},
                ],
            ],
        },
        {
            'label': '_not_a_size',
            'on_match': not_a_size,
            'patterns': [
                [
                    {'LOWER': {'IN': _NOT_A_SIZE}},
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units'},
                ],
                [
                    {'LOWER': {'IN': _NOT_A_SIZE}},
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units', 'OP': '?'},
                    {'LOWER': {'IN': CROSS}},
                    {'ENT_TYPE': 'about', 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'length_units'},
                ],
            ],
        },
    ],
}
