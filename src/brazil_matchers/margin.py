"""Parse margin trait notations."""

from traiter.pylib.util import squash

from ..pylib.util import GROUP_STEP, TRAIT_STEP

MARGIN_KEY = """ margin margins """.split()
MARGIN_SHAPE = """ margin_shape surface """.split()
MARGIN_LEADER = """ margin_leader shape_leader """.split()
MARGIN_FOLLOWER = """ margin_follower """.split()


def margin_term(span):
    """Build up margin phrases."""
    return {'margin_term': span.lower_}


def margin(span):
    """Enrich a margin match."""
    data = {
        'subpart': 'margin',
        'margin': squash([t.lower_ for t in span
                          if t.ent_type_ in {'margin_term', 'surface'}])}
    return data


MARGIN = {
    GROUP_STEP: [
        {
            'label': 'margin_term',
            'on_match': margin_term,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': MARGIN_LEADER}, 'OP': '?'},
                    {'ENT_TYPE': 'margin_shape'},
                    {'ENT_TYPE': {'IN': MARGIN_FOLLOWER}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': {'IN': MARGIN_LEADER}},
                    {'ENT_TYPE': {'IN': MARGIN_FOLLOWER}},
                ],
            ],
        },
    ],
    TRAIT_STEP: [
        {
            'label': 'margin',
            'on_match': margin,
            'patterns': [
                [
                    {'LOWER': {'IN': MARGIN_KEY}},
                    {'ENT_TYPE': {'IN': MARGIN_SHAPE}},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'ENT_TYPE': 'margin_term', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': 'margin_term'},
                ],
                [
                    {'LOWER': {'IN': MARGIN_KEY}},
                    {'ENT_TYPE': {'IN': MARGIN_SHAPE}},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'ENT_TYPE': 'margin_term'},
                ],
                [
                    {'LOWER': {'IN': MARGIN_KEY}},
                    {'ENT_TYPE': 'margin_term'},
                ],
            ],
        },
    ],
}
