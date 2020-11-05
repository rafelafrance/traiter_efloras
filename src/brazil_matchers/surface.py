"""Parse surface trait notations."""

from traiter.pylib.util import squash

from ..pylib.util import PARTS, PRESENCE, PRESENT, REPLACE, SLASH, TRAIT_STEP

SURFACE_KEY = """ surface surfaces """.split()


def surface(span):
    """Enrich a surface match."""
    data = {}

    fields = {
        'present': set(),
        'subpart': set(),
        'surface': [],
    }

    for token in span:
        label = token.ent_type_
        if label in ('part', 'location'):
            data[label] = REPLACE.get(token.lower_, token.lower_)
        elif label == 'surface':
            fields['surface'].append(REPLACE.get(token.lower_, token.lower_))
        elif label == 'subpart':
            fields['subpart'].add(REPLACE.get(token.lower_, token.lower_))
        elif token.lower_ in PRESENT:
            fields['present'].add(PRESENCE.get(token.lower_, False))

    if len(fields['subpart']) > 1:
        fields['subpart'] -= {'surface'}

    fields = {k: squash(v) for k, v in fields.items() if fields[k]}
    data = {**data, **fields}

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
                [
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'ENT_TYPE': 'surface'},
                    {'TEXT': {'IN': SLASH}},
                    {'ENT_TYPE': 'surface'},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'LOWER': {'IN': SURFACE_KEY}},
                    {'ENT_TYPE': 'location', 'OP': '?'},
                ],
            ],
        },
    ],
}
