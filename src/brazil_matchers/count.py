"""Parse count notations."""

from traiter.pylib.util import to_positive_int

from ..pylib.util import GROUP_STEP, SLASH

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

    if field := [t.lower_ for t in span if t.ent_type_ == 'per_count']:
        data['per_count'] = field[0]

    if field := [t.lower_ for t in span if t.ent_type_ == 'part']:
        data['part'] = field[0]

    return data


COUNT = {
    GROUP_STEP: [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                [
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                # With per_count as a prefix
                [
                    {'ENT_TYPE': 'per_count'},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'per_count'},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'per_count'},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'per_count'},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'per_count'},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': 'part'},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}},
                    {'IS_DIGIT': True},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'TEXT': {'IN': MORE}, 'OP': '?'},
                ],
            ],
        },
    ],
}
