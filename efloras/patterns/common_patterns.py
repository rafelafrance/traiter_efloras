from traiter.const import CLOSE
from traiter.const import COMMA
from traiter.const import CROSS
from traiter.const import DASH
from traiter.const import FLOAT_TOKEN_RE
from traiter.const import OPEN
from traiter.const import PLUS
from traiter.const import SLASH

ABBREVS = """
    Jan. Feb. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
    ca. al. """.split()
AND = ["&", "and", "et"]
CONJ = ["or", "and"]
TO = ["to"]
UNDERLINE = ["_"]
MISSING = """
    no without missing lack lacking except excepting not rarely obsolete
    """.split()

COMMON_PATTERNS = {
    "any": {},
    "(": {"TEXT": {"IN": OPEN}},
    ")": {"TEXT": {"IN": CLOSE}},
    "-": {"TEXT": {"IN": DASH}, "OP": "+"},
    "-*": {"TEXT": {"IN": DASH}, "OP": "*"},
    "[+]": {"TEXT": {"IN": PLUS}},
    "/": {"TEXT": {"IN": SLASH}},
    ",": {"TEXT": {"IN": COMMA}},
    "x": {"TEXT": {"IN": CROSS}},
    "to": {"LOWER": {"IN": TO}},
    "-/or": {"LOWER": {"IN": DASH + TO + CONJ}, "OP": "+"},
    "-/to": {"LOWER": {"IN": DASH + TO}, "OP": "+"},
    "and": {"LOWER": {"IN": AND}},
    "and/or": {"LOWER": {"IN": CONJ}},
    "missing": {"LOWER": {"IN": MISSING}},
    "9": {"IS_DIGIT": True},
    "99.9": {"TEXT": {"REGEX": FLOAT_TOKEN_RE}},
    "99-99": {"ENT_TYPE": {"REGEX": "^range"}},
    "99.9-99.9": {"ENT_TYPE": {"REGEX": "^range"}},
    "phrase": {"LOWER": {"REGEX": r"^([^.;:]+)$"}},
    "clause": {"LOWER": {"REGEX": r"^([^.;:,]+)$"}},
}

FORGET = """ about cross color_mod dim dimension imperial_length imperial_mass
    joined margin_leader metric_length metric_mass not_a_range per_count
    quest shape_leader shape_suffix surface units range
    """.split()

TRAITS = set(
    """ color color_mod count location margin_shape part
    size shape sex subpart woodiness part_as_loc """.split()
)
