"""Plant part is being  used as a location parser."""

from ..pylib.util import GROUP_STEP


def not_a_part_location(_):
    """Flag this as a token to be deleted."""
    return {'_forget': True}


PART_LOCATION = {
    GROUP_STEP: [
        {
            'label': 'not_a_part_location',
            'on_match': not_a_part_location,
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': ['sex', 'sex_enclosed', 'location']}},
                    {'ENT_TYPE': 'part'},
                ],
            ],
        },
        {
            'label': 'part_location',
            'patterns': [
                [
                    {'POS': {'IN': ['PART', 'ADP', 'VERB', 'SCONJ']}},
                    {'ENT_TYPE': 'part'},
                ],
            ],
        },
    ],
}
