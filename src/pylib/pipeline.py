"""Create a trait pipeline."""

import spacy
from traiter.pattern_utils import add_ruler_patterns
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
from src.patterns.reject import REJECT
from src.patterns.shape import SHAPE
from src.patterns.shared import SHARED
from src.patterns.size import SIZE
from src.patterns.subpart import SUBPART
from src.patterns.subpart_linker import SUBPART_LINKER
from src.patterns.suffix_count import SUFFIX_COUNT
from src.pylib.consts import TERMS

MATCHERS = [COUNT_PHRASE, MARGIN_SHAPE, PART_LOCATION, SHAPE, SIZE, SUFFIX_COUNT]

TERM_MATCHERS = [RANGE, SHARED]
ENTITY_MATCHERS = [COLOR, COUNT, DESCRIPTOR, PART, PHRASE, REJECT, SUBPART]
LINKERS = [PART_LINKER, SUBPART_LINKER]

DEBUG_COUNT = 0


def trait_pipeline():
    """Setup the pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner', 'lemmatizer'])
    add_debug_pipes(nlp, 'after tokenizer', entities=False)  # #######################
    add_term_ruler_pipe(nlp)
    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe('cache_label', after='term_merger')
    # add_debug_pipes(nlp, 'after term_merger')  # ###################################
    add_match_ruler_pipe(nlp)
    # add_debug_pipes(nlp, 'after match_ruler')  # ###################################
    add_entity_data_pipe(nlp)
    # add_debug_pipes(nlp, 'after entity_data')  # ###################################
    add_linker_pipe(nlp)
    # add_debug_pipes(nlp)    # ######################################################
    return nlp


def add_term_ruler_pipe(nlp):
    """Add a pipe to identify phrases and patterns as base-level traits."""
    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe(
        'entity_ruler', name='term_ruler', config=config, before='parser')
    term_ruler.add_patterns(TERMS.for_entity_ruler())
    add_ruler_patterns(term_ruler, *TERM_MATCHERS)


def add_match_ruler_pipe(nlp):
    """Add a pipe to group tokens into larger traits."""
    config = {'overwrite_ents': True}
    match_ruler = nlp.add_pipe('entity_ruler', name='match_ruler', config=config)
    add_ruler_patterns(match_ruler, *ENTITY_MATCHERS)


def add_entity_data_pipe(nlp):
    """Add a pipe that adds data to entities."""
    config = {'actions': EntityData.from_matchers(*ENTITY_MATCHERS)}
    nlp.add_pipe('entity_data', config=config)


def add_linker_pipe(nlp):
    """Add a pipe for linking body parts with other traits."""
    config = {'patterns': LINKERS}
    nlp.add_pipe('dependency', name='part_linker', config=config)


def add_debug_pipes(nlp, message='', tokens=True, entities=True):
    """Add pipes for debugging."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    config = {'message': message}
    if tokens:
        nlp.add_pipe('debug_tokens', name=f'debug_tokens{DEBUG_COUNT}', config=config)
    if entities:
        nlp.add_pipe(
            'debug_entities', name=f'debug_entities{DEBUG_COUNT}', config=config)
