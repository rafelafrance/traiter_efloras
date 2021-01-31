"""Traits to reject."""

from traiter.entity_data_util import REJECT_MATCH


REJECTS = """ color_mod dimension imperial_length imperial_mass metric_mass 
    shape_leader shape_suffix surface """.split()

FORGET = [
    {
        'label': 'color_mod',
        'on_match': REJECT_MATCH,
        'patterns': [[{'ENT_TYPE': {'IN': REJECTS}, 'OP': '+'}]],
    },
]
