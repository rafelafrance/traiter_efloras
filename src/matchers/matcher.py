"""Base matcher object."""

from traiter.matcher import TraitMatcher  # pylint: disable=import-error

from .all_matchers import MATCHERS
from ..pylib.terms import TERMS
from ..pylib.util import ATTACH_STEP, GROUP_STEP, TRAIT_STEP


class Matcher(TraitMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    name = 'entity_matcher'

    def __init__(self, nlp, attach=True):
        super().__init__(nlp)

        self.add_terms(TERMS)

        groups = []
        traits = []
        attaches = []

        for matcher in MATCHERS:
            groups += matcher.get(GROUP_STEP, [])
            traits += matcher.get(TRAIT_STEP, [])
            attaches += matcher.get(ATTACH_STEP, [])

        self.add_patterns(groups, GROUP_STEP)
        self.add_patterns(traits, TRAIT_STEP)
        if attach:
            self.add_patterns(attaches, ATTACH_STEP)
