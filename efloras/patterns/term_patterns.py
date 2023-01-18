import re

from traiter.terms.db import Db

from ..pylib import const

TERM_DB = const.DATA_DIR / "plant_terms.sqlite"

if not TERM_DB.exists():
    TERM_DB = const.MOCK_DIR / "plant_terms.sqlite"

TERMS = Db.shared("colors units")
TERMS += Db.select_term_set(TERM_DB, "plant_treatment")
TERMS += Db.hyphenate_terms(TERMS)
TERMS += Db.trailing_dash(TERMS, label="color")
TERMS.drop("imperial_length")

REPLACE = TERMS.pattern_dict("replace")
REMOVE = TERMS.pattern_dict("remove")

# #########################################################################
# Used to filter paragraphs in the source documents.

PARA_RE = [t["pattern"] for t in TERMS.with_label("part")]
PARA_RE = "|".join(PARA_RE)
PARA_RE = re.compile(PARA_RE)

# #########################################################################
PARTS = """
    female_flower_part
    flower_part
    fruit_part
    inflorescence
    leaf_part
    male_flower_part
    multiple_parts
    part
    """.split()
PARTS_SET = set(PARTS)

LOCATIONS = """ location flower_location part_as_loc subpart_as_loc """.split()

SUBPARTS = ["subpart", "subpart_suffix"]
SUBPART_SET = set(SUBPARTS)

TRAITS = (
    LOCATIONS
    + SUBPARTS
    + """
    color
    color_mod
    count
    duration
    habit
    habitat
    joined
    margin_shape
    reproduction
    sex
    shape
    size
    woodiness
""".split()
)
TRAITS_SET = set(TRAITS)

ALL_TRAITS = LOCATIONS + PARTS + SUBPARTS + TRAITS
ALL_TRAITS_SET = set(ALL_TRAITS)


def all_traits_except(removes: list[str]) -> list:
    return [t for t in ALL_TRAITS if t not in removes]
