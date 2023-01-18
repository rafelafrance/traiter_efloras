from traiter.patterns import matcher_patterns

from . import common_patterns
from . import term_patterns

PART_PARENTS = ["part"]
PART_CHILDREN = term_patterns.all_traits_except(["part"])

PART_LINKER = matcher_patterns.MatcherPatterns(
    "part_linker",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": PART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": PART_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)

# ####################################################################################
LINK_PART_ONCE_PARENTS = PART_PARENTS
LINK_PART_ONCE_CHILDREN = ["size", "count"]
LINK_PART_ONCE = matcher_patterns.MatcherPatterns(
    "link_part_once",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": LINK_PART_ONCE_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LINK_PART_ONCE_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)
