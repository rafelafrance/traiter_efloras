"""Parse count notations."""

from traiter.pylib.util import to_positive_int

from ..pylib.util import TRAIT_STEP, SLASH

COUNT_KEY = """ count number """.split()
MORE = """ more """.split()
PARTS = """ part subpart """.split()


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
    if field := [t.lower_ for t in span if t.ent_type_ == 'subpart']:
        data['subpart'] = field[0]

    return data


COUNT = {
    TRAIT_STEP: [
        {
            'label': 'count',
            'on_match': count,
            'patterns': [
                # Example: number of the pairs of the leaflet 1/2/3/4/5
                [
                    {'LOWER': {'IN': COUNT_KEY}},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': 'per_count', 'OP': '?'},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'IS_DIGIT': True, 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'IS_DIGIT': True, 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'IS_DIGIT': True, 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'IS_DIGIT': True, 'OP': '?'},
                ],
                # Example: count of the pairs of the leaflet 1/2/3/4/5 or more
                [
                    {'LOWER': {'IN': COUNT_KEY}},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': 'per_count', 'OP': '?'},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'IS_DIGIT': True},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'IS_DIGIT': True, 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'IS_DIGIT': True, 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'IS_DIGIT': True, 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'IS_DIGIT': True, 'OP': '?'},
                    {'POS': 'CCONJ', 'OP': '?'},
                    {'LOWER': {'IN': MORE}},
                ],
            ],
        },
    ],
}
