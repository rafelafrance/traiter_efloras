"""Plant part parser."""

from ..pylib.util import TRAIT_STEP, COLON, REPLACE


def part(span):
    """Enrich the parse."""
    part_ = span[0].lower_
    return {'part': REPLACE.get(part_, part_)}


PART = {
    TRAIT_STEP: [
        {
            'label': 'part',
            'on_match': part,
            'patterns': [
                [
                    {'ENT_TYPE': 'part'},
                    {'TEXT': {'IN': COLON}},
                ],
            ],
        },
    ],
}
