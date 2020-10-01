"""Plant part is being  used as a location parser."""

from ..pylib.util import GROUP_STEP

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
