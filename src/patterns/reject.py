"""Traits to reject."""

from traiter.pipes.entity_data import REJECT_MATCH


REJECT = [
    {
        'label': 'color_mod',
        'on_match': REJECT_MATCH,
        'patterns': [
            [{'ENT_TYPE': 'color_mod', 'OP': '+'}],
            [{'ENT_TYPE': 'shape_leader', 'OP': '+'}],
            [{'ENT_TYPE': 'imperial_length', 'OP': '+'}],
            [{'ENT_TYPE': 'imperial_mass', 'OP': '+'}],
            [{'ENT_TYPE': 'metric_mass', 'OP': '+'}],
        ],
    },
]
