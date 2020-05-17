"""Base matcher object."""

from traiter.matcher import Parser

from .plant_color import PLANT_COLOR
from .plant_part import PLANT_PART
from ..pylib.catalog import TERMS


class Base(Parser):
    """Base matcher object."""

    def __init__(self):
        super().__init__()

        self.add_terms(TERMS)

        traits = {**PLANT_PART, **PLANT_COLOR}
        self.add_traits(traits)
