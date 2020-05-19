"""Utilities for working with traits."""

import regex
from traiter.util import as_list

from ..matchers.plant_color import PLANT_COLOR
from ..matchers.plant_descriptor import PLANT_DESCRIPTOR
from ..matchers.plant_part import PLANT_PART
from ..matchers.plant_shape import PLANT_SHAPE

MATCHERS = [PLANT_COLOR, PLANT_DESCRIPTOR, PLANT_PART, PLANT_SHAPE]

MATCHER_NAMES = {m['name']: m for m in MATCHERS}
TRAIT2MATCHER = {n: m['name'] for m in MATCHERS for n in m['trait_names']}
TRAIT_NAMES = sorted(TRAIT2MATCHER.keys())


def expand_trait_names(trait_names):
    """Expand traits wildcards like: * or ?."""
    trait_names = as_list(trait_names) if trait_names else list(TRAIT2MATCHER)
    trait_names += ['plant_part']  # We always need to parse plant_parts

    traits = set()
    for name in trait_names:
        pattern = name.replace('*', '.*').replace('?', '.?')
        pattern = regex.compile(pattern, regex.IGNORECASE)
        hits = {t for t in TRAIT2MATCHER if pattern.search(t)}
        traits |= hits

    return sorted(traits)


def traits_to_matchers(trait_names):
    """Given a set of trait names return the corresponding matchers."""
    matcher_names = sorted({TRAIT2MATCHER[n] for n in trait_names})
    return [MATCHER_NAMES[n] for n in matcher_names]
