"""Parse count notations."""

from traiter.pylib.util import to_positive_int

from ..pylib.util import GROUP_STEP, SLASH

OR = ' or '.split()
MORE = ' more '.split()


def count(span):
    """Enrich the pattern match with data."""
    data = {}

    values = [to_positive_int(t.text) for t in span if t.is_digit]

    if len(values) == 1:
        data['low'] = values[0]
    elif len(values) == values[-1] - values[0] + 1:
        data['low'] = values[0]
        data['high'] = values[-1]
    else:
        data['values'] = values

    if any(t.lower_ in MORE for t in span):
        data['more'] = True

    return data


COUNT = {
    GROUP_STEP: [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': OR}, 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': OR}, 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': OR}, 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': OR}, 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': OR}, 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
            ],
        },
    ],
}
