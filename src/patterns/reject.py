"""Traits to reject."""

from traiter.pipes.entity_data import REJECT_MATCH


REJECTS = """ color_mod shape_leader imperial_length imperial_mass metric_mass 
    surface shape_suffix """.split()

REJECT = [
    {
        'label': 'color_mod',
        'on_match': REJECT_MATCH,
        'patterns': [[{'ENT_TYPE': {'IN': REJECTS}, 'OP': '+'}]],
    },
]
