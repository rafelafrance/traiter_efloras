"""Base matcher object."""

from spacy.language import Language
from traiter.spacy_nlp.matcher import SpacyMatcher

from .count import COUNT
from .shape import SHAPE
from .size import SIZE
from ..pylib.util import GROUP_STEP, TERMS, TRAIT_STEP

MATCHERS = [COUNT, SHAPE, SIZE]


class Matcher(SpacyMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    name: str = 'brazil_matcher'

    def __init__(self, nlp: Language, training: bool = False):
        super().__init__(nlp)

        self.add_terms(TERMS)

        if not training:
            self.add_patterns(MATCHERS, GROUP_STEP)
            self.add_patterns(MATCHERS, TRAIT_STEP)
