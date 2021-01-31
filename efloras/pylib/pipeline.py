"""Create a trait pipeline."""

import spacy
from traiter.entity_data_util import from_matchers
from traiter.pattern_util import add_ruler_patterns
from traiter.pipes.debug import DEBUG_ENTITIES, DEBUG_TOKENS
from traiter.pipes.dependency import Dependency
from traiter.pipes.new_entity_data import NEW_ENTITY_DATA
# from traiter.pipes.sentence import SENTENCE
from traiter.pipes.simple_entity_data import SIMPLE_ENTITY_DATA

from efloras.patterns.color import COLOR
from efloras.patterns.count import COUNT
from efloras.patterns.forget import FORGET
from efloras.patterns.margin import MARGIN_SHAPE
from efloras.patterns.part_linker import PART_LINKER
from efloras.patterns.range import RANGE
from efloras.patterns.sex_linker import SEX_LINKER
from efloras.patterns.shape import SHAPE
from efloras.patterns.size import SIZE
from efloras.patterns.subpart_linker import SUBPART_LINKER
from efloras.patterns.suffix_count import SUFFIX_COUNT
from efloras.pylib.const import REPLACE, TERMS

MATCHERS = [MARGIN_SHAPE, SUFFIX_COUNT]

TERM_MATCHERS = [RANGE]
ENTITY_MATCHERS = [COLOR, COUNT, FORGET, SHAPE, SIZE]
LINKERS = [PART_LINKER, SEX_LINKER, SUBPART_LINKER]

DEBUG_COUNT = 0  # Used to rename debug pipes


def trait_pipeline():
    """Setup the pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner', 'lemmatizer'])
    # add_debug_pipes(nlp, 'after tokenizer')  # #####################################
    add_term_ruler_pipe(nlp)
    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe(SIMPLE_ENTITY_DATA, after='term_merger', config={'replace': REPLACE})
    # add_debug_pipes(nlp, 'before match_ruler')  # ##################################
    add_match_ruler_pipe(nlp)
    add_debug_pipes(nlp, 'before entity_data', entities=True)  # ###################
    add_entity_data_pipe(nlp)
    add_debug_pipes(nlp, 'after entity_data', entities=True)  # ####################
    add_linker_pipe(nlp)
    # add_debug_pipes(nlp, 'after linker', entities=True)  # #########################
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
    config = {'actions': from_matchers(*ENTITY_MATCHERS)}
    nlp.add_pipe(NEW_ENTITY_DATA, config=config)


def add_linker_pipe(nlp):
    """Add a pipe for linking body parts with other traits."""
    config = {
        'patterns': LINKERS,
        'after_match': Dependency.after_match_args(*LINKERS),
    }
    nlp.add_pipe('dependency', name='part_linker', config=config)


def add_debug_pipes(nlp, message='', tokens=True, entities=False):
    """Add pipes for debugging."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    config = {'message': message}
    if tokens:
        nlp.add_pipe(DEBUG_TOKENS, name=f'tokens{DEBUG_COUNT}', config=config)
    if entities:
        nlp.add_pipe(DEBUG_ENTITIES, name=f'entities{DEBUG_COUNT}', config=config)
