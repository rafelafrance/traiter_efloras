"""Common color snippets."""
import re

from spacy import registry
from traiter.const import DASH
from traiter.const import DASH_CHAR
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

MULTIPLE_DASHES = ["\\" + c for c in DASH_CHAR]
MULTIPLE_DASHES = rf'\s*[{"".join(MULTIPLE_DASHES)}]{{2,}}\s*'

SKIP = DASH + common_patterns.MISSING

COLOR = MatcherPatterns(
    "color",
    on_match="efloras.color.v1",
    decoder=common_patterns.COMMON_PATTERNS
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
    parts = []
    for token in ent:
        replace = term_patterns.REPLACE.get(token.lower_, token.lower_)
        if replace in SKIP:
            continue
        if term_patterns.REMOVE.get(token.lower_):
            continue
        if token.pos_ in ["AUX"]:
            continue
        parts.append(replace)
    value = "-".join(parts)
    value = re.sub(MULTIPLE_DASHES, r"-", value)
    ent._.data["color"] = term_patterns.REPLACE.get(value, value)
    if any(t for t in ent if t.lower_ in common_patterns.MISSING):
        ent._.data["missing"] = True
