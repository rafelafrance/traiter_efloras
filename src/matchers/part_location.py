"""Plant part is being  used as a location parser."""

from ..pylib.util import TRAIT_STEP


def part_location(span):
    """Handle a part that is being used as a location."""
    return {'location': span.lower_, '_skip': True}


PART_LOCATION = {
    TRAIT_STEP: [
        {
            'label': 'part_location',
            'on_match': part_location,
            'patterns': [[
                {'POS': {'IN': ['PART', 'ADP', 'VERB', 'SCONJ']}},
                {'ENT_TYPE': 'part'},
            ]],
        },
    ],
}
