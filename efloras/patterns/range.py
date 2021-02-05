"""Shared range patterns."""

from traiter.matcher_compiler import MatcherCompiler
from traiter.pipe_util import REJECT_MATCH

from ..pylib.const import COMMON_PATTERNS

COMPILE = MatcherCompiler(COMMON_PATTERNS)

RANGE = [
    {
        'label': 'range.low',
        'patterns': COMPILE('99.9'),
    },
    {
        'label': 'range.min.low',
        'patterns': COMPILE(
            '( 99.9 -/or ) 99.9',
            '( 99.9 -/to ) 99.9',
        ),
    },
    {
        'label': 'range.low.high',
        'patterns': COMPILE(
            '99.9 and/or 99.9',
            '99.9 -/to   99.9',
        ),
    },
    {
        'label': 'range.low.max',
        'patterns': COMPILE(
            '99.9 ( and/or 99.9 )',
            '99.9 ( -/to   99.9 )',
        ),
    },
    {
        'label': 'range.min.low.high',
        'patterns': COMPILE(
            '( 99.9   -/or )   99.9 -/to     99.9',
            '( 99.9   -/or )   99.9 - and/or 99.9',
            '( 99.9   and/or ) 99.9   and/or 99.9',
            '  99.9 ( and/or   99.9    -/to  99.9 )',
        ),
    },
    {
        'label': 'range.min.low.max',
        'patterns': COMPILE(
            '( 99.9 - ) 99.9 - ( -/to 99.9 )',
            '  99.9 -   99.9 - ( -/to 99.9 )',
            '  99.9 - and/or 99.9 -/to 99.9',
        ),
    },
    {
        'label': 'range.low.high.max',
        'patterns': COMPILE(
            '99.9 ( and/or 99.9 -/or 99.9 )',
            '99.9 - 99.9   ( -/to 99.9 )',
            '99.9 - 99.9 - ( -/to 99.9 )',
            '99.9 - 99.9 - 99.9',
            '99.9 -/to 99.9 and/or 99.9',
            '99.9 - and/or 99.9 ( -/or 99.9 )',
            '99.9 and/or 99.9 ( and/or 99.9 )',
        ),
    },
    {
        'label': 'range.min.low.high.max',
        'patterns': COMPILE(
            '( 99.9 - ) 99.9 - 99.9 ( -/to 99.9 )',
            '( 99.9 -/or ) 99.9 - and/or 99.9 ( -/or 99.9 )',
            '( 99.9 and/or ) 99.9 - and/or 99.9 ( and/or 99.9 )',
            '99.9 - and/or 99.9 - and/or 99.9 -/to 99.9',
            '99.9 - and/or 99.9 -/to 99.9 ( -/or 99.9 )',
            '99.9 -/to 99.9 ( -/or 99.9 ) ( -/or 99.9 )',
            '99.9 99.9 -/to and/or 99.9 ( -/or 99.9 )',
            '99.9 and/or 99.9 - 99.9 ( -/or 99.9 )',
        ),
    },
    {
        'label': 'not_a_range',
        'on_match': REJECT_MATCH,
        'patterns': COMPILE(
            '9 / 9',
        ),
    },
]
