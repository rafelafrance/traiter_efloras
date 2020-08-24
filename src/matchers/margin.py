"""Parse the trait."""
from .shared import DASH
from ..pylib.util import TRAIT_STEP

_LEADERS = """ shape shape_leader margin_leader """.split()
_FOLLOWERS = """ shape margin_shape margin_follower """.split()
_SHAPES = """ margin_shape shape """.split()
_KEEP = set(_SHAPES)


def margin(span):
    """Enrich a phrase match."""
    data = {}
    value = [t.lower_ for t in span if t.ent_type_ in _KEEP]
    data['margin_shape'] = '-'.join(value)
    return data


MARGIN_SHAPE = {
    TRAIT_STEP: [
        {
            'label': 'margin_shape',
            'on_match': margin,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': _LEADERS}, 'OP': '*'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': 'margin_shape', 'OP': '+'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': {'IN': _FOLLOWERS}, 'OP': '*'},
                ],
                [
                    {'ENT_TYPE': {'IN': _SHAPES}, 'OP': '+'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'ENT_TYPE': {'IN': _FOLLOWERS}, 'OP': '+'},
                ],
            ],
        },
    ],
}
