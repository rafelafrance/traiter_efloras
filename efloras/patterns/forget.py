"""Traits to reject."""

from traiter.actions import REJECT_MATCH
from traiter.patterns.matcher_patterns import MatcherPatterns

from efloras.pylib.const import COMMON_PATTERNS

REJECTS = """ about color_mod dimension imperial_length imperial_mass
    margin_leader metric_length metric_mass not_a_range per_count quest
    shape_leader shape_suffix surface """.split()

FORGET = MatcherPatterns(
    REJECT_MATCH,
    on_match=REJECT_MATCH,
    decoder=COMMON_PATTERNS | {
        'reject': {'ENT_TYPE': {'IN': REJECTS}}
    },
    patterns=[
        'reject',
        '99-99',
    ],
)
