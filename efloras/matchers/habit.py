"""Plant habit snippets."""

from ..pylib.terms import REPLACE, TERMS

HABIT_LABELS = {t['label'] for t in TERMS if t['category'] == 'habit'}
HABIT_LABELS = sorted(HABIT_LABELS)


def habit(span):
    """Enrich the match."""
    value = span.lower_

    return dict(
        habit=REPLACE.get(value, value),
        _relabel=span[0]._.label,
        start=span.start_char,
        end=span.end_char,
    )


HABIT = {
    'name': 'habit',
    'matchers': [
        {
            'label': 'habit',
            'on_match': habit,
            'patterns': [[
                {'_': {'label': {'IN': HABIT_LABELS}}},
            ]],
        },
    ]
}
