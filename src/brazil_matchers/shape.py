"""Parse shape traits."""

from traiter.pylib.util import squash

from ..pylib.util import REPLACE, SLASH, TRAIT_STEP

SHAPE_KEY = """ form shape """.split()
PARTS = ['part', 'subpart']


def shape(span):
    """Enrich a phrase match."""
    data = {'shape': squash([REPLACE.get(t.lower_, t.lower_) for t in span
                             if t.ent_type_ == 'shape'])}

    if field := [t.lower_ for t in span if t.ent_type_ == 'part']:
        data['part'] = field[0]
    if field := [t.lower_ for t in span if t.ent_type_ == 'subpart']:
        data['subpart'] = field[0]

    return data


SHAPE = {
    TRAIT_STEP: [
        {
            'label': 'shape',
            'on_match': shape,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'ENT_TYPE': 'shape'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                ],
                [
                    {'LOWER': {'IN': SHAPE_KEY}},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'ENT_TYPE': 'shape'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'shape', 'OP': '?'},
                ],
            ],
        },
    ],
}
