"""Create a trait pipeline."""

import spacy
from traiter.pattern_utils import add_ruler_patterns
from traiter.tokenizer_utils import add_tokenizer
from traiter.pipes import cache, debug, dependency, sentence
from traiter.pipes.entity_data import EntityData

from src.patterns.color import COLOR
from src.patterns.count import COUNT
from src.patterns.count_phrase import COUNT_PHRASE
from src.patterns.descriptor import DESCRIPTOR
from src.patterns.margin import MARGIN_SHAPE
from src.patterns.part import PART
from src.patterns.part_linker import PART_LINKER
from src.patterns.part_location import PART_LOCATION
from src.patterns.phrase import PHRASE
from src.patterns.range import RANGE
from src.patterns.shape import SHAPE
from src.patterns.shared import SHARED
from src.patterns.size import SIZE
from src.patterns.subpart import SUBPART
from src.patterns.suffix_count import SUFFIX_COUNT
from src.pylib.consts import TERMS

MATCHERS = [
    COLOR, COUNT, COUNT_PHRASE, DESCRIPTOR, MARGIN_SHAPE, PART, PART_LOCATION,
    PHRASE, RANGE, SHAPE, SHARED, SIZE, SUBPART, SUFFIX_COUNT]

MATCHERS1 = [RANGE, SHARED]
MATCHERS2 = [COLOR, PART]
ALL_MATCHERS = MATCHERS1 + MATCHERS2

LINKERS = [PART_LINKER]


def trait_pipeline():
    """Setup the pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner', 'lemmatizer'])
    # add_tokenizer(nlp)
    add_term_ruler_pipe(nlp)
    # nlp.add_pipe('debug_tokens', name='debug_tokens1')
    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe('cache_label', after='term_merger')
    add_match_ruler_pipe(nlp)
    nlp.add_pipe('debug_tokens', name='debug_tokens2')
    nlp.add_pipe('debug_entities', name='debug_entities2')
    add_entity_data_pipe(nlp)
    add_linker_pipe(nlp)
    return nlp


def add_term_ruler_pipe(nlp):
    """Add a pipe to identify phrases and patterns as base-level traits."""
    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe(
        'entity_ruler', name='term_ruler', config=config, before='parser')
    term_ruler.add_patterns(TERMS.for_entity_ruler())
    add_ruler_patterns(term_ruler, *MATCHERS1)


def add_match_ruler_pipe(nlp):
    """Add a pipe to group tokens into larger traits."""
    config = {'overwrite_ents': True}
    match_ruler = nlp.add_pipe('entity_ruler', name='match_ruler', config=config)
    add_ruler_patterns(match_ruler, *MATCHERS2)


def add_entity_data_pipe(nlp):
    """Add a pipe that adds data to entities."""
    config = {'actions': EntityData.from_matchers(*ALL_MATCHERS)}
    nlp.add_pipe('entity_data', config=config)


def add_linker_pipe(nlp):
    """Add a pipe for linking body parts with other traits."""
    config = {'patterns': LINKERS}
    nlp.add_pipe('dependency', name='part_linker', config=config)


# class Pipeline(SpacyPipeline):
#     """Build a custom traiter pipeline."""
#
#     def __init__(self) -> None:
#         super().__init__()
#
#         self.nlp.disable_pipes(['ner'])
#
#         token2entity = {TRAIT_STEP}
#
#         Term.add_pipes(self.nlp, TERMS, before='parser')
#         Rule.add_pipe(self.nlp, MATCHERS, GROUP_STEP, before='parser')
#         Rule.add_pipe(self.nlp, MATCHERS, TRAIT_STEP, before='parser')
#         Sentencizer.add_pipe(self.nlp, ABBREVS, before='parser')
#         LinkMatcher.add_pipe(self.nlp, MATCHERS, LINK_STEP, before='parser')
#         ToEntities.add_pipe(self.nlp, token2entity=token2entity, before='parser')
