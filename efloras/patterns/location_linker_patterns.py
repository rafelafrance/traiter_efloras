"""Link traits to body parts."""
from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes.dependency_pipe import LINK_NEAREST

from ..pylib import const
from ..pylib import util

TRAITS_ = util.remove_traits(const.TRAITS, "location")

LOCATION_LINKER = DependencyPatterns(
    "location_linker",
    on_match={"func": LINK_NEAREST, "kwargs": {"anchor": "location"}},
    decoder={
        "location": {"ENT_TYPE": "location"},
        "trait": {"ENT_TYPE": {"IN": TRAITS_}},
        "link": {"POS": {"IN": ["ADJ", "AUX", "VERB"]}},
    },
    patterns=[
        "location <  trait",
        "location .  trait",
        "location >> trait",
        "location .  trait >> trait",
        "location .  link  >> trait",
        "location <  link  >> trait",
        "location >  link  >> trait",
        "location <  trait >> trait",
    ],
)
