"""Common size snippets."""

import re

import spacy
from traiter.const import CROSS, FLOAT_RE
from traiter.pipes.entity_data import REJECT_MATCH
from traiter.util import to_positive_float

from ..pylib.const import IS_RANGE, REPLACE

_FOLLOW = """ dimension sex """.split()
_NOT_A_SIZE = """ for """.split()

SIZE = [
    {
        'label': 'size',
        'on_match': 'size.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length'},
                {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
            ],
            [
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length', 'OP': '?'},
                {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                {'LOWER': {'IN': CROSS}},
                {'LOWER': 'to', 'OP': '?'},
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length'},
                {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
            ],
            [
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length', 'OP': '?'},
                {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                {'LOWER': {'IN': CROSS}},
                {'LOWER': 'to', 'OP': '?'},
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length', 'OP': '?'},
                {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
                {'LOWER': {'IN': CROSS}},
                {'LOWER': 'to', 'OP': '?'},
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length'},
                {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
            ],
        ],
    },
    {
        'label': 'size.high_only',
        'on_match': 'size_high_only.v1',
        'patterns': [
            [
                {'LOWER': 'to'},
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'LOWER': {'REGEX': FLOAT_RE}},
                {'ENT_TYPE': 'quest', 'OP': '?'},
                {'ENT_TYPE': 'metric_length'},
                {'ENT_TYPE': {'IN': _FOLLOW}, 'OP': '*'},
            ],
        ],
    },
    {
        'label': 'size.double_dim',
        'on_match': 'size_double_dim.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length'},
                {'ENT_TYPE': {'IN': 'sex_enclosed' 'sex'}, 'OP': '?'},
                {'ENT_TYPE': 'dimension'},
                {'LOWER': 'and'},
                {'ENT_TYPE': 'dimension'},
            ],
        ],
    },
    {
        'label': '_not_a_size',
        'on_match': REJECT_MATCH,
        'patterns': [
            [
                {'LOWER': {'IN': _NOT_A_SIZE}},
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length'},
            ],
            [
                {'LOWER': {'IN': _NOT_A_SIZE}},
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length', 'OP': '?'},
                {'LOWER': {'IN': CROSS}},
                {'ENT_TYPE': 'about', 'OP': '?'},
                {'ENT_TYPE': IS_RANGE},
                {'ENT_TYPE': 'metric_length'},
            ],
        ],
    },
]


def _size(ent, high_only=False):
    """Enrich a phrase match."""
    dims = scan_tokens(ent, high_only)
    dims = fix_dimensions(dims)
    data = fill_data(dims)
    ent._.new_label = 'size'
    ent._.data = data
    return data


@spacy.registry.misc(SIZE[0]['on_match'])
def size(ent):
    """Enrich a phrase match."""
    _size(ent)


@spacy.registry.misc(SIZE[1]['on_match'])
def size_high_only(ent):
    """Enrich a phrase match."""
    _size(ent, True)


@spacy.registry.misc(SIZE[2]['on_match'])
def size_double_dim(ent):
    """Handle the case when the dimensions are doubled but values are not.

    Like: Legumes 2.8-4.5 mm high and wide
    """
    data = _size(ent)
    print(data)
    dims = [REPLACE.get(t.lower_, t.lower_) for t in ent
            if t._.cached_label == 'dimension']

    new_data = {}
    for key, value in data.items():
        parts = key.split('_')
        if parts[0] in dims:
            parts[0] = dims[1] if parts[0] == dims[0] else dims[0]
            new_key = '_'.join(parts)
            new_data[new_key] = value

    ent._.data = {**data, **new_data}


def scan_tokens(ent, high_only):
    """Scan tokens for the various fields."""
    dims = [{}]

    for token in ent:
        label = token._.cached_label.split('.')[0]

        if label == 'range':
            values = re.findall(FLOAT_RE, token.text)
            values = [to_positive_float(v) for v in values]
            keys = token._.cached_label.split('.')[1:]
            for key, value in zip(keys, values):
                dims[-1][key] = value
            if high_only:
                dims[-1]['high'] = dims[-1]['low']
                del dims[-1]['low']

        elif label == 'metric_length':
            dims[-1]['units'] = REPLACE[token.lower_]

        elif label == 'dimension':
            dims[-1]['dimension'] = REPLACE[token.lower_]

        elif label == 'sex':
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
