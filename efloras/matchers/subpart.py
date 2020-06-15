"""Plant subpart parser."""

from ..pylib.terms import REPLACE


def subpart(span):
    """Enrich a plant subpart match."""
    value = REPLACE.get(span.lower_, span.lower_)
    return dict(subpart=value)


SUBPART = {
    'name': 'subpart',
    'matchers': [
        {
            'label': 'subpart',
            'on_match': subpart,
            'patterns': [[
                {'_': {'label': 'subpart'}}
            ]],
        },
    ],
}
