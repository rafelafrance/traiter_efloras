"""Plant part is being  used as a location parser."""

from .consts import GROUP_STEP

PART_LOCATION = {
    GROUP_STEP: [
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
