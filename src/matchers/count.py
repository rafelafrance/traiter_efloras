"""Common count snippets."""

from traiter.actions import forget

from ..pylib.consts import CLOSE, CROSS, OPEN, REPLACE, SLASH, TRAIT_STEP

_NO_COUNTS = (CROSS + SLASH
              + """ average side times days weeks by """.split())
_NO_COUNT = set(_NO_COUNTS)

_COUNT_KILLER = """ length_units mass_units """.split()

PARENS = OPEN + CLOSE


def count(span):
    """Enrich the match with data."""
    data = {}

    for token in span:
        label = token.ent_type_

        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}

        elif label == 'per_count':
            data['group'] = REPLACE.get(token.lower_, token.lower_)

        elif token.lower_ in PARENS:
            continue

        elif token.lower_ in {'of'}:
            continue

        else:
            return

    return data


COUNT = {
    TRAIT_STEP: [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'ENT_TYPE': 'range'},
                    {'ENT_TYPE': 'per_count', 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'per_count'},
                    {'LOWER': {'IN': ['of']}, 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                ],
                [
                    {'TEXT': {'IN': OPEN}},
                    {'ENT_TYPE': 'range'},
                    {'TEXT': {'IN': CLOSE}},
                    {'ENT_TYPE': 'per_count', 'OP': '?'},
                ],
            ],
        },
        {
            'label': '_not_a_count',
            'on_match': forget,
            'patterns': [
                [
                    {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                    {'ENT_TYPE': 'range'},
                    {'LOWER': {'IN': _NO_COUNTS}, 'OP': '?'},
                    {'ENT_TYPE': {'IN': _COUNT_KILLER}, 'OP': '?'},
                    {'ENT_TYPE': 'range', 'OP': '?'},
                ],
            ],
        },
    ],
}
