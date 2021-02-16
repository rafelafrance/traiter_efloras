"""Shared range patterns."""

from traiter.actions import REJECT_MATCH
from traiter.patterns.matcher_patterns import MatcherPatterns

from efloras.pylib.const import COMMON_PATTERNS

DECODER = COMMON_PATTERNS | {
    'ambiguous': {'LOWER': {'IN': ['few', 'many']}},
}

RANGE_LOW = MatcherPatterns(
    'range.low',
    decoder=DECODER,
    patterns=[
        '99.9',
        '( 99.9 -/or ) ambiguous ( -/to ambiguous )',
    ],
)

RANGE_MIN_LOW = MatcherPatterns(
    'range.min.low',
    decoder=DECODER,
    patterns=[
        '( 99.9 -/or ) 99.9',
        '( 99.9 -/to ) 99.9',
    ],
)

RANGE_LOW_HIGH = MatcherPatterns(
    'range.low.high',
    decoder=DECODER,
    patterns=[
        '99.9 and/or 99.9',
        '99.9 -/to   99.9',
    ],
)

RANGE_LOW_MAX = MatcherPatterns(
    'range.low.max',
    decoder=DECODER,
    patterns=[
        '99.9 ( and/or 99.9 )',
        '99.9 ( -/to   99.9 )',
    ],
)

RANGE_MIN_LOW_HIGH = MatcherPatterns(
    'range.min.low.high',
    decoder=DECODER,
    patterns=[
        '( 99.9   -/or )   99.9 -/to     99.9',
        '( 99.9   -/or )   99.9 - and/or 99.9',
        '( 99.9   and/or ) 99.9   and/or 99.9',
        '  99.9 ( and/or   99.9    -/to  99.9 )',
    ],
)

RANGE_MIN_LOW_MAX = MatcherPatterns(
    'range.min.low.max',
    decoder=DECODER,
    patterns=[
        '( 99.9 - ) 99.9 -? ( -/to 99.9 [+]? )',
        '  99.9 -   99.9 - ( -/to 99.9 )',
        '  99.9 - and/or 99.9 -/to 99.9',
    ],
)

RANGE_LOW_HIGH_MAX = MatcherPatterns(
    'range.low.high.max',
    decoder=DECODER,
    patterns=[
        '99.9 ( and/or 99.9 -/or 99.9 [+]? )',
        '99.9 - 99.9   ( -/to 99.9 [+]? )',
        '99.9 - 99.9 - ( -/to 99.9 [+]? )',
        '99.9 - 99.9 - 99.9',
        '99.9 -/to 99.9 and/or 99.9',
        '99.9 - and/or 99.9 ( -/or 99.9 [+]? )',
        '99.9 and/or 99.9 ( and/or 99.9 [+]? )',
    ],
)

RANGE_MIN_LOW_HIGH_MAX = MatcherPatterns(
    'range.min.low.high.max',
    decoder=DECODER,
    patterns=[
        '( 99.9 - ) 99.9 - 99.9 ( -/to 99.9 [+]? )',
        '( 99.9 -/or ) 99.9 - and/or 99.9 ( -/or 99.9 [+]? )',
        '( 99.9 and/or ) 99.9 - and/or 99.9 ( and/or 99.9 [+]? )',
        '99.9 - and/or 99.9 - and/or 99.9 -/to 99.9',
        '99.9 - and/or 99.9 -/to 99.9 ( -/or 99.9 [+]? )',
        '99.9 -/to 99.9 ( -/or 99.9 ) ( -/or 99.9 [+]? )',
        '99.9 99.9 -/to and/or 99.9 ( -/or 99.9 [+]? )',
        '99.9 and/or 99.9 - 99.9 ( -/or 99.9 [+]? )',
    ],
)

NOT_A_RANGE = MatcherPatterns(
    'not_a_range',
    on_match=REJECT_MATCH,
    decoder=DECODER,
    patterns=[
        '9 / 9',
    ],
)
