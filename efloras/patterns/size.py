"""Common size snippets."""

import re

import spacy
from traiter.const import CROSS, FLOAT_RE
from traiter.matcher_compiler import MatcherCompiler
from traiter.pipe_util import REJECT_MATCH
from traiter.util import to_positive_float

from ..pylib.const import COMMON_PATTERNS, REPLACE

FOLLOW = """ dimension sex """.split()
NOT_A_SIZE = """ for """.split()

COMPILE = MatcherCompiler(COMMON_PATTERNS | {
    '[?]': {'ENT_TYPE': 'quest'},
    'about': {'ENT_TYPE': 'about'},
    'and': {'LOWER': 'and'},
    'cm': {'ENT_TYPE': 'metric_length'},
    'dim': {'ENT_TYPE': 'dimension'},
    'follow': {'ENT_TYPE': {'IN': FOLLOW}},
    'not_size': {'LOWER': {'IN': NOT_A_SIZE}},
    'sex': {'ENT_TYPE': 'sex'},
    'x': {'LOWER': {'IN': CROSS}},
})

SIZE = [
    {
        'label': 'size',
        'on_match': 'size.v1',
        'patterns': COMPILE(
            'about? 99.9-99.9 cm follow*',

            ('      about? 99.9-99.9 cm? follow* '
             'x to? about? 99.9-99.9 cm  follow*'),

            ('      about? 99.9-99.9 cm? follow* '
             'x to? about? 99.9-99.9 cm? follow* '
             'x to? about? 99.9-99.9 cm  follow*'),
        ),
    },
    {
        'label': 'size.high_only',
        'on_match': 'size_high_only.v1',
        'patterns': COMPILE(
            'to about? 99.9 [?]? cm follow*',
        ),
    },
    {
        'label': 'size.double_dim',
        'on_match': 'size_double_dim.v1',
        'patterns': COMPILE(
            'about? 99.9-99.9 cm  sex? ,? dim and dim',
            'about? 99.9-99.9 cm? sex? ,? 99.9-99.9 cm dim and dim',
        ),
    },
    {
        'label': '_not_a_size',
        'on_match': REJECT_MATCH,
        'patterns': COMPILE(
            'not_size about? 99.9-99.9 cm',
            'not_size about? 99.9-99.9 cm? x about? 99.9-99.9 cm',
        ),
    },
]


def _size(ent, high_only=False):
    """Enrich a phrase match."""
    dims = scan_tokens(ent, high_only)
    dims = fix_dimensions(dims)
    dims = fix_units(dims)
    fill_data(dims, ent)


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
    dims = [REPLACE.get(t.lower_, t.lower_) for t in ent
            if t._.cached_label == 'dimension']

    ranges = [e for e in ent.ents if e._.cached_label.split('.')[0] == 'range']

    for dim, range_ in zip(dims, ranges):
        _size(range_)
        new_data = {}
        for key, value in range_._.data.items():
            key_parts = key.split('_')
            if key_parts[-1] in ('low', 'high', 'max', 'min'):
                new_key = f'{dim}_{key_parts[-1]}'
                new_data[new_key] = value
            else:
                new_data[key] = value
        range_._.data = new_data


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


def fix_units(dims):
    """Fill in missing units."""
    default = [d.get('units') for d in dims][-1]
    for dim in dims:
        dim['units'] = dim.get('units', default)
    return dims


def fill_data(dims, ent):
    """Move fields into correct place & give them consistent names."""
    ranges = [e for e in ent.ents if e._.cached_label.split('.')[0] == 'range']

    for dim, range_ in zip(dims, ranges):
        data = {}
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

        range_._.data = data
        range_._.new_label = 'size'
