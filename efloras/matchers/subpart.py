"""Plant subpart parser."""

from ..pylib.terms import REPLACE, TERMS

_SEX = {t['pattern']: t['replace'] for t in TERMS if t['label'] in ('sex', )}


def subpart(span):
    """Enrich a plant subpart match."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label
        value = token.lower_
        if label == 'subpart':
            data['subpart'] = REPLACE.get(value, value)
        elif label == 'sex':
            data['sex'] = _SEX[value]
        elif label == 'location':
            data['location'] = value

    return data


SUBPART = {
    'name': 'subpart',
    'matchers': [
        {
            'label': 'subpart',
            'on_match': subpart,
            'patterns': [[
                {'_': {'label': {'IN': ['sex', 'location']}}, 'OP': '*'},
                {'_': {'label': 'subpart'}}
            ]],
        },
    ],
}
