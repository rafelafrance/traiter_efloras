"""Parse morphism trait notations."""

from ..pylib.util import PARTS, REPLACE, TRAIT_STEP


def morphism(span):
    """Enrich the trait."""
    data = {}
    for token in span:
        label = token.ent_type_
        if label in ('part', 'subpart'):
            data[label] = REPLACE.get(token.lower_, token.lower_)
        elif label == 'morphic':
            data['morphism'] = REPLACE.get(token.lower_, token.lower_)
    return data


MORPHISM = {
    TRAIT_STEP: [
        {
            'label': 'morphism',
            'on_match': morphism,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'ENT_TYPE': 'morphic'},
                ],
            ],
        },
    ],
}
