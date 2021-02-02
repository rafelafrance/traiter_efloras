"""Traits to reject."""

from traiter.pipe_util import REJECT_MATCH
from ..pylib.const import IS_RANGE


REJECTS = """ color_mod dimension imperial_length imperial_mass metric_mass 
    shape_leader shape_suffix surface per_count """.split()

FORGET = [
    {
        'label': 'color_mod',
        'on_match': REJECT_MATCH,
        'patterns': [
            [{'ENT_TYPE': {'IN': REJECTS}, 'OP': '+'}],
            [{'ENT_TYPE': IS_RANGE}],
        ],
    },
]
