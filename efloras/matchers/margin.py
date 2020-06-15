"""Parse the trait."""
from .shared import DASH

_LEADERS = """ shape shape_leader """.split()
_KEEP = {'margin_shape', 'shape'}


def margin(span):
    """Enrich a phrase match."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )
    value = [t.lower_ for t in span if t._.label in _KEEP]
    data['margin_shape'] = '-'.join(value)
    return data


MARGIN_SHAPE = {
    'name': 'margin_shape',
    'matchers': [
        {
            'label': 'margin_shape',
            'on_match': margin,
            'patterns': [
                [
                    {'_': {'label': {'IN': _LEADERS}}, 'OP': '*'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'_': {'label': 'margin_shape'}, 'OP': '+'},
                    {'TEXT': {'IN': DASH}, 'OP': '?'},
                    {'_': {'label': 'margin_shape'}, 'OP': '?'},
                ],
            ],
        },
    ]
}
