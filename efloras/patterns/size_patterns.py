"""Common size snippets."""
import re
from collections import deque

from spacy import registry
from traiter import const as t_const
from traiter import util as t_util
from traiter.actions import REJECT_MATCH
from traiter.const import CROSS
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

FOLLOW = """ dim sex """.split()
NOT_A_SIZE = """ for """.split()
SIZE_FIELDS = """ min low high max """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "[?]": {"ENT_TYPE": "quest"},
    "about": {"ENT_TYPE": "about"},
    "and": {"LOWER": "and"},
    "cm": {"ENT_TYPE": "metric_length"},
    "dim": {"ENT_TYPE": "dim"},
    "follow": {"ENT_TYPE": {"IN": FOLLOW}},
    "not_size": {"LOWER": {"IN": NOT_A_SIZE}},
    "sex": {"ENT_TYPE": "sex"},
    "x": {"LOWER": {"IN": CROSS}},
}

SIZE = MatcherPatterns(
    "size",
    on_match="efloras.size.v1",
    decoder=DECODER,
    patterns=[
        "about? 99.9-99.9 cm  follow*",
        "about? 99.9-99.9 cm? follow* " "x to? about? 99.9-99.9 cm  follow*",
        (
            "      about? 99.9-99.9 cm? follow* "
            "x to? about? 99.9-99.9 cm? follow* "
            "x to? about? 99.9-99.9 cm  follow*"
        ),
    ],
)

SIZE_HIGH_ONLY = MatcherPatterns(
    "size.high_only",
    on_match="efloras.size_high_only.v1",
    decoder=DECODER,
    patterns=[
        "to about? 99.9 [?]? cm follow*",
    ],
)

SIZE_DOUBLE_DIM = MatcherPatterns(
    "size.double_dim",
    on_match="efloras.size_double_dim.v1",
    decoder=DECODER,
    patterns=[
        "about? 99.9-99.9 cm  sex? ,? dim and dim",
        "about? 99.9-99.9 cm? sex? ,? 99.9-99.9 cm dim and dim",
    ],
)

NOT_A_SIZE = MatcherPatterns(
    "not_a_size",
    on_match=REJECT_MATCH,
    decoder=DECODER,
    patterns=[
        "not_size about? 99.9-99.9 cm",
        "not_size about? 99.9-99.9 cm? x about? 99.9-99.9 cm",
    ],
)


@registry.misc(SIZE.on_match)
def size(ent):
    """Enrich a phrase match."""
    _size(ent)


@registry.misc(SIZE_HIGH_ONLY.on_match)
def size_high_only(ent):
    """Enrich a phrase match."""
    _size(ent, True)


@registry.misc(SIZE_DOUBLE_DIM.on_match)
def size_double_dim(ent):
    """Handle the case when the dimensions are doubled but values are not.

    Like: Legumes 2.8-4.5 mm high and wide
    """
    dims = [
        term_patterns.REPLACE.get(t.lower_, t.lower_)
        for t in ent
        if t.ent_type_ == "dim"
    ]

    ranges = [e for e in ent.ents if e.label_ == "range"]

    for dim, range_ in zip(dims, ranges):
        _size(range_)
        for key, value in range_._.data.items():
            key_parts = key.split("_")
            if key_parts[-1] in SIZE_FIELDS:
                new_key = f"{dim}_{key_parts[-1]}"
                ent._.data[new_key] = value
            else:
                ent._.data[key] = value
    if "range" in ent._.data:
        del ent._.data["range"]
    ent._.new_label = "size"


def _size(ent, high_only=False):
    """Enrich a phrase match."""
    dims = scan_tokens(ent, high_only)
    dims = fix_dimensions(dims)
    dims = fix_units(dims)
    ent._.new_label = "size"
    fill_data(dims, ent)


def scan_tokens(ent, high_only):
    dims = [{}]

    for token in ent:
        label = token.ent_type_

        if label == "range":
            for field in SIZE_FIELDS:
                if field in token._.data:
                    dims[-1][field] = t_util.to_positive_float(token._.data[field])

            if high_only:
                dims[-1]["high"] = dims[-1]["low"]
                del dims[-1]["low"]

        elif label == "metric_length":
            dims[-1]["units"] = term_patterns.REPLACE[token.lower_]

        elif label == "dim":
            dims[-1]["dimension"] = term_patterns.REPLACE[token.lower_]

        elif label == "sex":
            dims[-1]["sex"] = re.sub(r"\W+", "", token.lower_)

        elif label == "quest":
            dims[-1]["uncertain"] = True

        elif token.lower_ in t_const.CROSS:
            dims.append({})

    return dims


def fix_dimensions(dims):
    """Handle when width comes before length & one of them is missing units."""
    noted = [d for n in dims if (d := n.get("dimension"))]
    defaults = deque(d for d in ("length", "width", "thickness") if d not in noted)

    for dim in dims:
        if not dim.get("dimension"):
            dim["dimension"] = defaults.popleft()

    return dims


def fix_units(dims):
    """Fill in missing units."""
    default = [d.get("units") for d in dims][-1]

    for dim in dims:
        dim["units"] = dim.get("units", default)

    return dims


def fill_data(dims, ent):
    """Move fields into correct place & give them consistent names."""
    # Need to find entities using their character offsets
    for dim in dims:
        dimension = dim["dimension"]

        for field in SIZE_FIELDS:
            if datum := dim.get(field):
                key = f"{dimension}_{field}"
                ent._.data[key] = round(datum, 3)

        if datum := dim.get("units"):
            key = f"{dimension}_units"
            ent._.data[key] = datum.lower()

        if datum := dim.get("sex"):
            ent._.data["sex"] = datum

        if dim.get("uncertain"):
            ent._.data["uncertain"] = "true"
