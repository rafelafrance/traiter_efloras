"""Create a trait pipeline."""

import spacy
from traiter.patterns.matcher_patterns import add_ruler_patterns, as_dicts
from traiter.pipes.add_entity_data import ADD_ENTITY_DATA
from traiter.pipes.debug import DEBUG_ENTITIES, DEBUG_TOKENS
from traiter.pipes.dependency import DEPENDENCY
from traiter.pipes.simple_entity_data import SIMPLE_ENTITY_DATA
from traiter.pipes.update_entity_data import UPDATE_ENTITY_DATA
from traiter.tokenizer_util import append_abbrevs, append_tokenizer_regexes

from efloras.patterns.color import COLOR
from efloras.patterns.count import COUNT, COUNT_WORD, NOT_A_COUNT
from efloras.patterns.forget import FORGET
from efloras.patterns.margin import MARGIN_SHAPE
from efloras.patterns.part_linker import PART_LINKER
from efloras.patterns.range import (
    NOT_A_RANGE, RANGE_LOW, RANGE_LOW_HIGH, RANGE_LOW_HIGH_MAX, RANGE_LOW_MAX,
    RANGE_MIN_LOW, RANGE_MIN_LOW_HIGH, RANGE_MIN_LOW_HIGH_MAX, RANGE_MIN_LOW_MAX)
from efloras.patterns.sex_linker import SEX_LINKER
from efloras.patterns.shape import N_SHAPE, SHAPE
from efloras.patterns.size import SIZE, SIZE_HIGH_ONLY, SIZE_DOUBLE_DIM, NOT_A_SIZE
from efloras.patterns.subpart_linker import SUBPART_LINKER
from efloras.pylib.const import ABBREVS, REPLACE, TERMS

TERM_RULES = [
    RANGE_LOW, RANGE_MIN_LOW, RANGE_LOW_HIGH, RANGE_LOW_MAX, RANGE_MIN_LOW_HIGH,
    RANGE_MIN_LOW_MAX, RANGE_LOW_HIGH_MAX, RANGE_MIN_LOW_HIGH_MAX, NOT_A_RANGE]
ADD_DATA = [COLOR, FORGET, MARGIN_SHAPE, N_SHAPE, SHAPE]
UPDATE_DATA = [
    COUNT, COUNT_WORD, NOT_A_COUNT, SIZE, SIZE_HIGH_ONLY, SIZE_DOUBLE_DIM, NOT_A_SIZE]

DEBUG_COUNT = 0  # Used to rename debug pipes


def pipeline():
    """Create a pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner', 'lemmatizer'])
    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, ABBREVS)

    # add_debug_pipes(nlp, 'after tokenizer')  # #####################################

    # Add a pipe to identify phrases and patterns as base-level traits.
    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe(
        'entity_ruler', name='term_ruler', config=config, before='parser')
    term_ruler.add_patterns(TERMS.for_entity_ruler())
    add_ruler_patterns(term_ruler, TERM_RULES)

    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe(SIMPLE_ENTITY_DATA, after='term_merger', config={'replace': REPLACE})

    # add_debug_pipes(nlp, 'before update_entities', entities=True)  # ################

    config = {'patterns': as_dicts(UPDATE_DATA)}
    nlp.add_pipe(UPDATE_ENTITY_DATA, name='update_entities', config=config)

    # add_debug_pipes(nlp, 'after update_entities', entities=True)  # #################

    # Add a pipe to group tokens into larger traits
    config = {'overwrite_ents': True}
    match_ruler = nlp.add_pipe('entity_ruler', name='match_ruler', config=config)
    add_ruler_patterns(match_ruler, ADD_DATA)

    # add_debug_pipes(nlp, 'before add_data', entities=True)  # ###################

    nlp.add_pipe(ADD_ENTITY_DATA, config={'patterns': as_dicts(ADD_DATA)})

    # add_debug_pipes(nlp, 'after add_data', entities=True)  # ####################

    config = {'patterns': as_dicts([PART_LINKER, SEX_LINKER, SUBPART_LINKER])}
    nlp.add_pipe(DEPENDENCY, name='part_linker', config=config)

    # add_debug_pipes(nlp, 'done', entities=True)  # #########################
    return nlp


def add_debug_pipes(nlp, message='', tokens=True, entities=False):
    """Add pipes for debugging."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    config = {'message': message}
    if tokens:
        nlp.add_pipe(DEBUG_TOKENS, name=f'tokens{DEBUG_COUNT}', config=config)
    if entities:
        nlp.add_pipe(DEBUG_ENTITIES, name=f'entities{DEBUG_COUNT}', config=config)
