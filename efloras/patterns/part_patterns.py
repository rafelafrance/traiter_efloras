from spacy import registry
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

PART_LEADER = """ primary secondary """.split()

PART_CHANGE = [p for p in term_patterns.PARTS if p != "part"]

DECODER = common_patterns.COMMON_PATTERNS | {
    "leader": {"LOWER": {"IN": PART_LEADER}},
    "part": {"ENT_TYPE": {"IN": term_patterns.PARTS}},
}

# ####################################################################################
PART = MatcherPatterns(
    "part",
    on_match="mimosa.part.v1",
    decoder=DECODER,
    patterns=[
        "leader? part",
        "leader? part -   part",
        "leader? part and part",
    ],
)


@registry.misc(PART.on_match)
def on_part_match(ent):
    key = [k for k in ent._.data.keys() if k in PART_CHANGE]
    if key:
        ent._.data["part"] = ent._.data[key[0]]
        del ent._.data[key[0]]

    ent._.new_label = "part"

    if any(t.lower_ in common_patterns.AND for t in ent):
        ent._.new_label = "multiple_parts"
        ent._.data["multiple_parts"] = [
            term_patterns.REPLACE.get(t.lower_, t.lower_)
            for t in ent
            if t.ent_type_ in term_patterns.PARTS_SET
        ]
