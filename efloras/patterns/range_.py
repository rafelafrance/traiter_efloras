"""Shared range patterns."""
import regex as re
from spacy import registry
from traiter import actions
from traiter.patterns.matcher_patterns import MatcherPatterns

from efloras.pylib.const import COMMON_PATTERNS

ON_RANGE_MATCH = "efloras.range.v1"

DECODER = COMMON_PATTERNS | {
    'ambiguous': {'LOWER': {'IN': ['few', 'many']}},
}

RANGE_LOW = MatcherPatterns(
    'range.low',
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        '99.9',
        '( 99.9 -/or ) ambiguous ( -/to ambiguous )',
    ],
)

RANGE_MIN_LOW = MatcherPatterns(
    'range.min.low',
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        '( 99.9 -/or ) 99.9',
        '( 99.9 -/to ) 99.9',
    ],
)

RANGE_LOW_HIGH = MatcherPatterns(
    'range.low.high',
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        '99.9 and/or 99.9',
        '99.9 -/to   99.9',
    ],
)

RANGE_LOW_MAX = MatcherPatterns(
    'range.low.max',
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        '99.9 ( and/or 99.9 )',
        '99.9 ( -/to   99.9 )',
    ],
)

RANGE_MIN_LOW_HIGH = MatcherPatterns(
    'range.min.low.high',
    on_match=ON_RANGE_MATCH,
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
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        '( 99.9 - ) 99.9 -? ( -/to 99.9 [+]? )',
        '  99.9 -   99.9 - ( -/to 99.9 )',
        '  99.9 - and/or 99.9 -/to 99.9',
    ],
)

RANGE_LOW_HIGH_MAX = MatcherPatterns(
    'range.low.high.max',
    on_match=ON_RANGE_MATCH,
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
    on_match=ON_RANGE_MATCH,
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
    on_match=actions.REJECT_MATCH,
    decoder=DECODER,
    patterns=[
        '9 / 9',
    ],
)


@registry.misc(ON_RANGE_MATCH)
def on_range_match(ent):
    keys = ent.label_.split(".")[1:]
    nums = [t.text for t in ent if re.match(r"^[\d.]+$", t.text)]

    # Reject big numbers
    if any(float(n) >= 1000.0 for n in nums):
        raise actions.RejectMatch()

    ent._.data = {k: v for k, v in zip(keys, nums)}
    for token in ent:
        token._.data = ent._.data

    ent._.new_label = "range"
