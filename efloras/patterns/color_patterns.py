"""Common color snippets."""
import re

from spacy import registry
from traiter.const import DASH
from traiter.const import DASH_CHAR
from traiter.patterns.matcher_patterns import MatcherPatterns

from ..pylib import const

MULTIPLE_DASHES = ["\\" + c for c in DASH_CHAR]
MULTIPLE_DASHES = rf'\s*[{"".join(MULTIPLE_DASHES)}]{{2,}}\s*'

SKIP = DASH + const.MISSING

COLOR = MatcherPatterns(
    "color",
    on_match="efloras.color.v1",
    decoder=const.COMMON_PATTERNS
    | {
        "color_words": {"ENT_TYPE": {"IN": ["color", "color_mod"]}},
        "color": {"ENT_TYPE": "color"},
        "to": {"POS": {"IN": ["AUX"]}},
    },
    patterns=[
        "missing? color_words* -* color+ -* color_words*",
        "missing? color_words+ to color_words+ color+ -* color_words*",
    ],
)


@registry.misc(COLOR.on_match)
def color(ent):
    """Enrich a phrase match."""
    parts = []
    for token in ent:
        replace = const.REPLACE.get(token.lower_, token.lower_)
        if replace in SKIP:
            continue
        if const.REMOVE.get(token.lower_):
            continue
        if token.pos_ in ["AUX"]:
            continue
        parts.append(replace)
    value = "-".join(parts)
    value = re.sub(MULTIPLE_DASHES, r"-", value)
    ent._.data["color"] = const.REPLACE.get(value, value)
    if any(t for t in ent if t.lower_ in const.MISSING):
        ent._.data["missing"] = True
