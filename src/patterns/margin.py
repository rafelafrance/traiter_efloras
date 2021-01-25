"""Parse the trait."""

import spacy
from traiter.consts import DASH

_LEADERS = """ shape shape_leader margin_leader """.split()
_FOLLOWERS = """ shape margin_shape margin_follower """.split()
_SHAPES = """ margin_shape shape """.split()
_KEEP = set(_SHAPES)


MARGIN_SHAPE = [
        {
            'label': 'margin_shape',
            'on_match': 'margin.v1',
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
]


@spacy.registry.misc(MARGIN_SHAPE[0]['on_match'])
def margin(span):
    """Enrich a phrase match."""
    data = {}
    value = [t.lower_ for t in span if t.ent_type_ in _KEEP]
    data['margin_shape'] = '-'.join(value)
    return data
