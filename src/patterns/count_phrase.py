"""Common suffix count snippets."""

import spacy
from traiter.util import to_positive_int

from ..pylib.consts import CATEGORY, REPLACE

COUNT_PHRASE = [
    {
        'label': 'count',
        'on_match': 'count_phrase.v1',
        'patterns': [
            [
                {'ENT_TYPE': 'count_word'},
            ],
        ],
    },
]


@spacy.registry.misc(COUNT_PHRASE[0]['on_match'])
def count_phrase(span):
    """Enrich the match with data."""
    data = {}

    count = to_positive_int(REPLACE.get(span.text, span.text))
    if count:
        data['low'] = count
    else:
        data['min'] = count

    if subpart := CATEGORY.get(span.text):
        data['_subpart'] = subpart

    return data
