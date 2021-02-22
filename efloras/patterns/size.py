"""Common size snippets."""

import re
from collections import deque

from spacy import registry
from traiter.actions import REJECT_MATCH
from traiter.const import CROSS, FLOAT_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import to_positive_float

from efloras.pylib.const import COMMON_PATTERNS, REPLACE

FOLLOW = """ dim sex """.split()
NOT_A_SIZE = """ for """.split()

DECODER = COMMON_PATTERNS | {
    '[?]': {'ENT_TYPE': 'quest'},
    'about': {'ENT_TYPE': 'about'},
    'and': {'LOWER': 'and'},
    'cm': {'ENT_TYPE': 'metric_length'},
    'dim': {'ENT_TYPE': 'dim'},
    'follow': {'ENT_TYPE': {'IN': FOLLOW}},
    'not_size': {'LOWER': {'IN': NOT_A_SIZE}},
    'sex': {'ENT_TYPE': 'sex'},
    'x': {'LOWER': {'IN': CROSS}},
}

SIZE = MatcherPatterns(
    'size',
    on_match='size.v1',
    decoder=DECODER,
    patterns=[
        'about? 99.9-99.9 cm follow*',

        ('      about? 99.9-99.9 cm? follow* '
         'x to? about? 99.9-99.9 cm  follow*'),

        ('      about? 99.9-99.9 cm? follow* '
         'x to? about? 99.9-99.9 cm? follow* '
         'x to? about? 99.9-99.9 cm  follow*'),
    ],
)

SIZE_HIGH_ONLY = MatcherPatterns(
    'size.high_only',
    on_match='size_high_only.v1',
    decoder=DECODER,
    patterns=[
        'to about? 99.9 [?]? cm follow*',
    ],
)

SIZE_DOUBLE_DIM = MatcherPatterns(
    'size.double_dim',
    on_match='size_double_dim.v1',
    decoder=DECODER,
    patterns=[
        'about? 99.9-99.9 cm  sex? ,? dim and dim',
        'about? 99.9-99.9 cm? sex? ,? 99.9-99.9 cm dim and dim',
    ],
)

NOT_A_SIZE = MatcherPatterns(
    'not_a_size',
    on_match=REJECT_MATCH,
    decoder=DECODER,
    patterns=[
        'not_size about? 99.9-99.9 cm',
        'not_size about? 99.9-99.9 cm? x about? 99.9-99.9 cm',
    ],
)


@registry.misc(SIZE.on_match)
def size(ent):
    """Enrich a phrase match."""
    _size(ent)


@registry.misc(SIZE_HIGH_ONLY.on_match)
def size_high_only(ent):
    """Enrich a phrase match."""
    _size(ent, True)


@registry.misc(SIZE_DOUBLE_DIM.on_match)
def size_double_dim(ent):
    """Handle the case when the dimensions are doubled but values are not.

    Like: Legumes 2.8-4.5 mm high and wide
    """
    dims = [REPLACE.get(t.lower_, t.lower_) for t in ent
            if t._.cached_label == 'dim']

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


def _size(ent, high_only=False):
    """Enrich a phrase match."""
    dims = scan_tokens(ent, high_only)
    dims = fix_dimensions(dims)
    dims = fix_units(dims)
    fill_data(dims, ent)


def scan_tokens(ent, high_only):
    """Scan tokens for the various fields."""
    dims = [{}]

    # Map token indices to the char span for the sub-entities
    token_2_ent = {(i - ent.start): (e.start_char, e.end_char)
                   for e in ent.ents for i in range(e.start, ent.end)}

    # Process tokens in the entity
    for t, token in enumerate(ent):
        label = token._.cached_label.split('.')[0]
        print(label)

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
            dims[-1]['units_link'] = token_2_ent[t]

        elif label == 'dim':
            dims[-1]['dimension'] = REPLACE[token.lower_]
            dims[-1]['dimension_link'] = token_2_ent[t]

        elif label == 'sex':
            dims[-1]['sex'] = re.sub(r'\W+', '', token.lower_)
            dims[-1]['sex_link'] = token_2_ent[t]

        elif label == 'quest':
            dims[-1]['uncertain'] = True
            dims[-1]['uncertain_link'] = token_2_ent[t]

        elif token.lower_ in CROSS:
            dims.append({})

    return dims


def fix_dimensions(dims):
    """Handle width comes before length and one of them is missing units."""
    noted = [d for n in dims if (d := n.get('dimension'))]
    defaults = deque(d for d in ('length', 'width', 'thickness') if d not in noted)

    for dim in dims:
        if not dim.get('dimension'):
            dim['dimension'] = defaults.popleft()

    return dims


def fix_units(dims):
    """Fill in missing units."""
    default = [d.get('units') for d in dims][-1]
    default_link = [d.get('units_link') for d in dims][-1]

    for dim in dims:
        dim['units'] = dim.get('units', default)
        dim['units_link'] = dim.get('units_link', default_link)

    return dims


def fill_data(dims, ent):
    """Move fields into correct place & give them consistent names."""
    # Need to find entities using their character offsets
    link_2_ent = {(e.start_char, e.end_char): e for e in ent.ents}

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

        if (link := dim.get('units_link')) is not None:
            range_._.links['units_link'] = [link]
            sub_ent = link_2_ent[link]
            sub_ent._.new_label = 'units'

        if (link := dim.get('dimension_link')) is not None:
            range_._.links['dimension_link'] = [link]
            sub_ent = link_2_ent[link]
            sub_ent._.new_label = 'dimension'

        if (link := dim.get('sex_link')) is not None:
            range_._.links['sex_link'] = [link]

        range_._.data = data
        range_._.new_label = 'size'
