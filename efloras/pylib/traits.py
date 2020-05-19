"""Utilities for working with traits."""

from ..matchers.plant_color import PLANT_COLOR
from ..matchers.plant_part import PLANT_PART
from ..matchers.plant_shape import PLANT_SHAPE

MATCHERS = [PLANT_COLOR, PLANT_PART, PLANT_SHAPE]

MATCHER_NAMES = {m['name']: m for m in MATCHERS}
TRAIT2MATCHER = {t: m['name'] for m in MATCHERS for t in m['trait_names']}
