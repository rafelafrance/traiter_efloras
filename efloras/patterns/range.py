"""Shared range patterns."""

from traiter.actions import REJECT_MATCH
from traiter.patterns.matcher_patterns import MatcherPatterns

from efloras.pylib.const import COMMON_PATTERNS

RANGE_LOW = MatcherPatterns(
    'range.low',
    decoder=COMMON_PATTERNS,
    patterns=['99.9'],
)

RANGE_MIN_LOW = MatcherPatterns(
    'range.min.low',
    decoder=COMMON_PATTERNS,
    patterns=[
        '( 99.9 -/or ) 99.9',
        '( 99.9 -/to ) 99.9',
    ],
)

RANGE_LOW_HIGH = MatcherPatterns(
    'range.low.high',
    decoder=COMMON_PATTERNS,
    patterns=[
        '99.9 and/or 99.9',
        '99.9 -/to   99.9',
    ],
)

RANGE_LOW_MAX = MatcherPatterns(
    'range.low.max',
    decoder=COMMON_PATTERNS,
    patterns=[
        '99.9 ( and/or 99.9 )',
        '99.9 ( -/to   99.9 )',
    ],
)

RANGE_MIN_LOW_HIGH = MatcherPatterns(
    'range.min.low.high',
    decoder=COMMON_PATTERNS,
    patterns=[
        '( 99.9   -/or )   99.9 -/to     99.9',
        '( 99.9   -/or )   99.9 - and/or 99.9',
        '( 99.9   and/or ) 99.9   and/or 99.9',
        '  99.9 ( and/or   99.9    -/to  99.9 )',
    ],
)

RANGE_MIN_LOW_MAX = MatcherPatterns(
    'range.min.low.max',
    decoder=COMMON_PATTERNS,
    patterns=[
        '( 99.9 - ) 99.9 - ( -/to 99.9 )',
        '  99.9 -   99.9 - ( -/to 99.9 )',
        '  99.9 - and/or 99.9 -/to 99.9',
    ],
)

RANGE_LOW_HIGH_MAX = MatcherPatterns(
    'range.low.high.max',
    decoder=COMMON_PATTERNS,
    patterns=[
        '99.9 ( and/or 99.9 -/or 99.9 )',
        '99.9 - 99.9   ( -/to 99.9 )',
        '99.9 - 99.9 - ( -/to 99.9 )',
        '99.9 - 99.9 - 99.9',
        '99.9 -/to 99.9 and/or 99.9',
        '99.9 - and/or 99.9 ( -/or 99.9 )',
        '99.9 and/or 99.9 ( and/or 99.9 )',
    ],
)

RANGE_MIN_LOW_HIGH_MAX = MatcherPatterns(
    'range.min.low.high.max',
    decoder=COMMON_PATTERNS,
    patterns=[
        '( 99.9 - ) 99.9 - 99.9 ( -/to 99.9 )',
        '( 99.9 -/or ) 99.9 - and/or 99.9 ( -/or 99.9 )',
        '( 99.9 and/or ) 99.9 - and/or 99.9 ( and/or 99.9 )',
        '99.9 - and/or 99.9 - and/or 99.9 -/to 99.9',
        '99.9 - and/or 99.9 -/to 99.9 ( -/or 99.9 )',
        '99.9 -/to 99.9 ( -/or 99.9 ) ( -/or 99.9 )',
        '99.9 99.9 -/to and/or 99.9 ( -/or 99.9 )',
        '99.9 and/or 99.9 - 99.9 ( -/or 99.9 )',
    ],
)

NOT_A_RANGE = MatcherPatterns(
    'not_a_range',
    on_match=REJECT_MATCH,
    decoder=COMMON_PATTERNS,
    patterns=[
        '9 / 9',
    ],
)
