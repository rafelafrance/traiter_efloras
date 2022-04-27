"""Link traits to a plant's sex.

We want to handle sexual dimorphism by linking traits to a plant's sex.
For example: "petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate):
Should note that pistillate petals are 3-10 mm and staminate petals are 5-8 mm.
Named entity recognition (NER) must be run first.
"""
from traiter.patterns.dependency_patterns import DependencyPatterns
from traiter.pipes.dependency_pipe import LINK_NEAREST

from efloras.pylib.const import TRAITS
from efloras.pylib.util import remove_traits

TRAITS_ = remove_traits(TRAITS, "sex")

SEX_LINKER = DependencyPatterns(
    "sex_linker",
    on_match={
        "func": LINK_NEAREST,
        "kwargs": {"anchor": "sex", "dir_bias": "after"},
    },
    decoder={
        "sex": {"ENT_TYPE": "sex"},
        "trait": {"ENT_TYPE": {"IN": TRAITS_}},
        "count": {"ENT_TYPE": "count"},
        "part": {"ENT_TYPE": "part"},
        "link": {"POS": {"IN": ["ADJ", "AUX", "VERB"]}},
        "mm": {"_": {"cached_label": "metric_length"}},
    },
    patterns=[
        "sex   >> trait",
        "sex   <  trait",
        "sex   .  trait",
        "sex   .  trait >> trait",
        "sex   .  link  >> trait",
        "sex   >  link  >> trait",
        "sex   <  trait >> trait",
        "sex   <  part  <  part",
        "sex   ;  part  <  link >> trait",
        "trait .  mm    .  sex",
    ],
)
