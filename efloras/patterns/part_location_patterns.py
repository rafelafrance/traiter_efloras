"""For when plant parts are being used as a location."""
from spacy import registry
from traiter.actions import TEXT_ACTION
from traiter.actions import text_action
from traiter.patterns.matcher_patterns import MatcherPatterns

from ..pylib import const

LOCATION_LEADERS = """
    to at embracing
    """.split()

DECODER = const.COMMON_PATTERNS | {
    "part": {"ENT_TYPE": "part"},
    "subpart": {"ENT_TYPE": "subpart"},
    "leader": {"LOWER": {"IN": LOCATION_LEADERS}},
    "not_loc": {"ENT_TYPE": {"IN": ["sex", "location"]}},
    "sex": {"ENT_TYPE": "sex"},
    "of": {"LOWER": "of"},
    "adj": {"POS": "ADJ"},
}

PART_AS_LOCATION = MatcherPatterns(
    "part_as_loc",
    on_match=TEXT_ACTION,
    decoder=DECODER,
    patterns=[
        "leader part",
    ],
)

SUBPART_AS_LOCATION = MatcherPatterns(
    "subpart_location",
    on_match="efloras.subpart_location.v1",
    decoder=DECODER,
    patterns=["leader subpart", "leader subpart of adj? subpart"],
)


@registry.misc(SUBPART_AS_LOCATION.on_match)
def subpart_location(ent):
    """Enrich the match with data."""
    ent._.new_label = "part_as_loc"
    text_action(ent)
