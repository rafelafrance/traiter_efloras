"""Base matcher object."""

from spacy.language import Language
from traiter.spacy_nlp.matcher import SpacyMatcher

from .attach import ATTACH
from .color import COLOR
from .count import COUNT
from .count_phrase import COUNT_PHRASE
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
from ..pylib.util import GROUP_STEP, SHARED, TERMS, TRAIT_STEP

MATCHERS = [
    ATTACH, COLOR, COUNT, COUNT_PHRASE, DESCRIPTOR, MARGIN_SHAPE,
    PART, PART_LOCATION, PHRASE, RANGE, SHAPE, SHARED, SIZE, SUBPART,
    SUFFIX_COUNT]


class Matcher(SpacyMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    name: str = 'entity_matcher'

    def __init__(self, nlp: Language, training: bool = False):
        super().__init__(nlp)

        self.add_terms(TERMS)

        if not training:
            self.add_patterns(MATCHERS, GROUP_STEP)
            self.add_patterns(MATCHERS, TRAIT_STEP)
