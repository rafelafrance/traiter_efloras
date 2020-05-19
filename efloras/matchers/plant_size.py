"""Common color snippets."""

import regex
from traiter.util import to_positive_float

from ..pylib.terms import TERMS

DIMENSIONS = {t['pattern']: t['category'] for t in TERMS
              if t['label'] == 'dimension'}
UNITS = {t['pattern']: t['category'] for t in TERMS
         if t['label'] == 'length_units'}
MULTIPLY = {t['category']: to_positive_float(m) for t in TERMS
            if t['label'] == 'length_units' if (m := t['replace'])}


def length(span):
    """Enrich a phrase match."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
        raw_value=span.text,
    )

    dims = [{}]
    d = 0

    for token in span:
        term = token._.term

        if term in 'min_size low_size high_size max_size'.split():
            key = term.split('_')[0]
            dims[d][key] = to_positive_float(token.text)

        elif term == 'length_units':
            units = UNITS[token.text.lower()]
            dims[d]['units'] = units
            dims[d]['times'] = MULTIPLY[units]

        elif term == 'dimension':
            dims[d]['dimension'] = DIMENSIONS[token.text.lower()]

        elif term == 'sex':
            value = token.text.lower()
            value = regex.sub(r'\W+', '', value)
            dims[d]['sex'] = value

        elif term == 'cross':
            d += 1
            dims.append({})

    if len(dims) > 1:
        if (dims[0].get('dimension') == 'width'
                or dims[1].get('dimension') == 'length'):
            dims[0], dims[1] = dims[1], dims[0]
        if not dims[0].get('times'):
            dims[0]['times'] = dims[1]['times']
        if not dims[1].get('times'):
            dims[1]['times'] = dims[0]['times']

    dims[0]['dim_name'] = dims[0].get('dimension', 'length')
    if len(dims) > 1:
        dims[1]['dim_name'] = dims[1].get('dimension', 'width')

    for dim in dims:
        dim_name = dim['dim_name']
        times = dim['times']
        for field in """ min low high max """.split():
            if value := dim.get(field):
                key = f'{dim_name}_{field}'
                data[key] = round(value * times, 3)
        if value := dim.get('sex'):
            data['sex'] = value.lower()
        if value := dim.get('units'):
            key = f'{dim_name}_units'
            data[key] = value.lower()

    return data


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
    'matchers': {
        'size': {
            'on_match': length,
            'patterns': [
                [
                    {'_': {'term': 'min_size'}, 'OP': '?'},
                    {'_': {'term': 'low_size'}},
                    {'_': {'term': 'high_size'}, 'OP': '?'},
                    {'_': {'term': 'max_size'}, 'OP': '?'},
                    {'_': {'term': 'length_units'}},
                    {'_': {'term': 'dimension'}, 'OP': '?'},
                    {'_': {'term': 'sex'}, 'OP': '?'},
                ],
                [
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
                ],
                [
                    {'_': {'term': 'high_size'}},
                    {'_': {'term': 'length_units'}},
                    {'_': {'term': 'dimension'}, 'OP': '?'},
                    {'_': {'term': 'sex'}, 'OP': '?'},
                ]
            ],
        },
    }
}
