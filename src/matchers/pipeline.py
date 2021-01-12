"""Create a trait pipeline."""

from traiter.matchers.rule import Rule
from traiter.matchers.term import Term
from traiter.pipeline import SpacyPipeline
from traiter.sentencizer import Sentencizer
from traiter.to_entities import ToEntities

from .color import COLOR
from .count import COUNT
from .count_phrase import COUNT_PHRASE
from .descriptor import DESCRIPTOR
from .link import LINK
from .link_matcher import LinkMatcher
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
from ..pylib.consts import ABBREVS, GROUP_STEP, LINK_STEP, TERMS, TRAIT_STEP

MATCHERS = [
    COLOR, COUNT, COUNT_PHRASE, DESCRIPTOR, LINK, MARGIN_SHAPE,
    PART, PART_LOCATION, PHRASE, RANGE, SHAPE, SHARED, SIZE, SUBPART,
    SUFFIX_COUNT]


class Pipeline(SpacyPipeline):
    """Build a custom traiter pipeline."""

    def __init__(self) -> None:
        super().__init__()

        self.nlp.disable_pipes(['ner'])

        token2entity = {TRAIT_STEP}

        Term.add_pipes(self.nlp, TERMS, before='parser')
        Rule.add_pipe(self.nlp, MATCHERS, GROUP_STEP, before='parser')
        Rule.add_pipe(self.nlp, MATCHERS, TRAIT_STEP, before='parser')
        Sentencizer.add_pipe(self.nlp, ABBREVS, before='parser')
        LinkMatcher.add_pipe(self.nlp, MATCHERS, LINK_STEP, before='parser')
        ToEntities.add_pipe(self.nlp, token2entity=token2entity, before='parser')
