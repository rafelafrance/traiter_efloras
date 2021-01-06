"""Common suffix count snippets."""

from traiter.pylib.util import to_positive_int  # pylint: disable=import-error

from ..pylib.consts import CATEGORY, REPLACE, TRAIT_STEP


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


COUNT_PHRASE = {
    TRAIT_STEP: [
        {
            'label': 'count',
            'on_match': count_phrase,
            'patterns': [
                [
                    {'ENT_TYPE': 'count_word'},
                ],
            ],
        },
    ],
}
