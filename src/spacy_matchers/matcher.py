"""Base matcher object."""

from traiter.spacy_nlp.matcher import SpacyMatcher

from .attach import ATTACH
from .color import COLOR
from .consts import GROUP_STEP, SHARED, TERMS, TRAIT_STEP
from .count import COUNT
from .descriptor import DESCRIPTOR
from .margin import MARGIN_SHAPE
from .part import PART
from .part_location import PART_LOCATION
from .phrase import PHRASE
from .range import RANGE
from .shape import SHAPE
from .size import SIZE
from .subpart import SUBPART
from .suffix_count import SUFFIX_COUNT

MATCHERS = [
    ATTACH, COLOR, COUNT, DESCRIPTOR, MARGIN_SHAPE, PART_LOCATION, PART,
    PHRASE, RANGE, SHAPE, SHARED, SIZE, SUBPART, SUFFIX_COUNT]


class Matcher(SpacyMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    name = 'entity_matcher'

    def __init__(self, nlp, training=False):
        super().__init__(nlp)

        self.add_terms(TERMS)

        if not training:
            self.add_patterns(MATCHERS, GROUP_STEP)
            self.add_patterns(MATCHERS, TRAIT_STEP)
