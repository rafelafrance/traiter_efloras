"""Parse surface trait notations."""

from traiter.pylib.util import squash

from ..pylib.util import PARTS, PRESENCE, PRESENT, REPLACE, SLASH, TRAIT_STEP

SURFACE_KEY = """ surface surfaces """.split()


def surface(span):
    """Enrich a surface match."""
    data = {}

    present = set()
    subparts = set()

    for token in span:
        label = token.ent_type_
        if label in ('part', 'surface', 'location'):
            data[label] = REPLACE.get(token.lower_, token.lower_)
        elif label == 'subpart':
            subparts.add(REPLACE.get(token.lower_, token.lower_))
        elif token.lower_ in PRESENT:
            present.add(PRESENCE.get(token.lower_, False))

    if len(subparts) > 1:
        subparts -= {'surface'}

    if subparts:
        data['subpart'] = squash(subparts)

    if present:
        data['present'] = squash(present)

    return data


SURFACE = {
    TRAIT_STEP: [
        {
            'label': 'surface',
            'on_match': surface,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'ENT_TYPE': 'surface'},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'LOWER': {'IN': SURFACE_KEY}},
                    {'ENT_TYPE': 'location', 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'LOWER': {'IN': PRESENT}},
                ],
                [
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'LOWER': {'IN': PRESENT}},
                    {'TEXT': {'IN': SLASH}},
                    {'LOWER': {'IN': PRESENT}},
                ],
                [
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'ENT_TYPE': 'surface'},
                ],
            ],
        },
    ],
}
