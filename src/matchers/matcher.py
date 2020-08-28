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
from .size import SIZE
from .subpart import SUBPART
from .suffix_count import SUFFIX_COUNT
from ..pylib.util import GROUP_STEP, TERMS, TRAIT_STEP

PARTS = [PART, SUBPART]
TRAITS = [
    ATTACH, COLOR, COUNT, DESCRIPTOR, MARGIN_SHAPE, PART_LOCATION, PHRASE,
    RANGE, SHAPE, SIZE, SUFFIX_COUNT]

MATCHERS = PARTS + TRAITS

LABELS = {t['label'] for m in MATCHERS for t in m.get(TRAIT_STEP, [])}

PART_LABELS = {p['label'] for p in PART.get(TRAIT_STEP, [])}
SUBPART_LABELS = {s['label'] for s in SUBPART.get(TRAIT_STEP, [])}
ALL_PARTS = PART_LABELS | SUBPART_LABELS


class Matcher(TraitMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    name = 'entity_matcher'

    def __init__(self, nlp):
        super().__init__(nlp)

        self.add_terms(TERMS)

        groups = TraitMatcher.step_rules(MATCHERS, GROUP_STEP)
        traits = TraitMatcher.step_rules(MATCHERS, TRAIT_STEP)

        self.add_patterns(groups, GROUP_STEP)
        self.add_patterns(traits, TRAIT_STEP)
