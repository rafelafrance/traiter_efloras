"""Parse inflorescence trait notations."""

from ..pylib.util import REPLACE, TRAIT_STEP

INFLORESCENCE_KEY = """ raceme """.split()


def inflorescence(span):
    """Enrich the trait."""
    data = {}
    for token in span:
        label = token.ent_type_
        if token.lower_ in INFLORESCENCE_KEY:
            data[label] = REPLACE.get(token.lower_, token.lower_)
        else:
            data['inflorescence'] = REPLACE.get(token.lower_, token.lower_)
    return data


INFLORESCENCE = {
    TRAIT_STEP: [
        {
            'label': 'inflorescence',
            'on_match': inflorescence,
            'patterns': [
                [
                    {'LOWER': {'IN': INFLORESCENCE_KEY}},
                    {'POS': {'IN': ['ADJ', 'NOUN']}},
                ],
            ],
        },
    ],
}
