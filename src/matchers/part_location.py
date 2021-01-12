"""Plant part is being  used as a location parser."""

from traiter.actions import forget

from ..pylib.consts import GROUP_STEP


PART_LOCATION = {
    GROUP_STEP: [
        {
            'label': 'not_a_part_location',
            'on_match': forget,
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
