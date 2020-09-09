"""Base matcher object."""

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from .attach import ATTACH
from .color import COLOR
from .count import COUNT
from .descriptor import DESCRIPTOR
from .margin import MARGIN_SHAPE
from .part import PART
from .part_location import PART_LOCATION
from .phrase import PHRASE
from .range import RANGE
from .shape import SHAPE
from .shared import SHARED
from .size import SIZE
from .subpart import SUBPART
from .suffix_count import SUFFIX_COUNT
from ..pylib.util import GROUP_STEP, TERMS, TRAIT_STEP

MATCHERS = [
    ATTACH, COLOR, COUNT, DESCRIPTOR, MARGIN_SHAPE, PART_LOCATION, PART,
    PHRASE, RANGE, SHAPE, SHARED, SIZE, SUBPART, SUFFIX_COUNT]


class Matcher(TraitMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    name = 'entity_matcher'

    def __init__(self, nlp):
        super().__init__(nlp)

        self.add_terms(TERMS)
        self.add_patterns(MATCHERS, GROUP_STEP)
        self.add_patterns(MATCHERS, TRAIT_STEP)
