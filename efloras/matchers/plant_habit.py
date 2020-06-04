"""Plant habit snippets."""

from ..pylib.terms import CATEGORY, REPLACE, TERMS

LABELS = """ habit habit_shape habitat woodiness """.split()

IS_HABIT = {t['pattern'] for t in TERMS
            if t['label'] in LABELS and t['category'] == 'habit'}


def habit(span):
    """Enrich the match."""
    token = span[0]
    value = token.lower_

    data = dict(
        value=REPLACE.get(value, ''),
        category=CATEGORY.get(value),
        start=span.start_char,
        end=span.end_char,
    )
    return data


PLANT_HABIT = {
    'name': 'habit',
    'matchers': [
        {
            'label': 'habit',
            'on_match': habit,
            'patterns': [[
                {'_': {'label': 'habit'}},
            ]],
        },
    ]
}
