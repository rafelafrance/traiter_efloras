"""Traits to reject."""

from traiter.pipe_util import REJECT_MATCH
from ..pylib.const import COMMON_PATTERNS
from traiter.matcher_compiler import MatcherCompiler


REJECTS = """ about color_mod dimension imperial_length imperial_mass
    margin_leader
    metric_length metric_mass not_a_range per_count quest
    shape_leader shape_suffix surface """.split()

COMPILE = MatcherCompiler(COMMON_PATTERNS | {
    'reject': {'ENT_TYPE': {'IN': REJECTS}}
})


FORGET = [
    {
        'label': 'color_mod',
        'on_match': REJECT_MATCH,
        'patterns': COMPILE(
            'reject',
            '99-99',
        ),
    },
]
