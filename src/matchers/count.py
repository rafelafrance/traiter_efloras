"""Common count snippets."""

from .shared import CROSS, PER_COUNT, PER_COUNTS, SLASH
from ..pylib.terms import REPLACE
from ..pylib.util import TRAIT_STEP

_NO_COUNTS = (CROSS + SLASH
              + """ average side times days weeks by """.split())
_NO_COUNT = set(_NO_COUNTS)

_COUNT_KILLER = """ length_units mass_units """.split()


def count(span):
    """Enrich the match with data."""
    data = {}

    for token in span:
        label = token.ent_type_

        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}

        elif token.lower_ in PER_COUNT:
            data['group'] = REPLACE.get(token.lower_, token.lower_)

        else:
            return {'_skip': True}

    return data


def not_a_count(span):
    """Flag this as a token to be deleted."""
    return {'_skip': True}


COUNT = {
    'name': 'count',
    TRAIT_STEP: [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'ENT_TYPE': 'range'},
                    {'LOWER': {'IN': PER_COUNTS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'not_a_count',
            'on_match': not_a_count,
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