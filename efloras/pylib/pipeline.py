"""Create a trait pipeline."""

import spacy
from traiter.pattern_util import add_ruler_patterns
from traiter.pipes.add_entity_data import ADD_ENTITY_DATA
from traiter.pipes.debug import DEBUG_ENTITIES, DEBUG_TOKENS
from traiter.pipes.dependency import DEPENDENCY
from traiter.pipes.simple_entity_data import SIMPLE_ENTITY_DATA
from traiter.pipes.update_entity_data import UPDATE_ENTITY_DATA
from traiter.tokenizer_util import append_abbrevs, append_tokenizer_regexes

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
from efloras.pylib.const import ABBREVS, REPLACE, TERMS

ENTITY_MATCHERS = [COLOR, FORGET, MARGIN_SHAPE, SHAPE]

DEBUG_COUNT = 0  # Used to rename debug pipes


def pipeline():
    """Setup the pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner', 'lemmatizer'])
    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, ABBREVS)

    # add_debug_pipes(nlp, 'after tokenizer')  # #####################################

    # Add a pipe to identify phrases and patterns as base-level traits.
    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe(
        'entity_ruler', name='term_ruler', config=config, before='parser')
    term_ruler.add_patterns(TERMS.for_entity_ruler())
    add_ruler_patterns(term_ruler, RANGE)

    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe(SIMPLE_ENTITY_DATA, after='term_merger', config={'replace': REPLACE})

    # add_debug_pipes(nlp, 'before update_entities', entities=True)  # ################

    config = {'patterns': [COUNT, SIZE]}
    nlp.add_pipe(UPDATE_ENTITY_DATA, name='update_entities', config=config)

    # add_debug_pipes(nlp, 'after update_entities', entities=True)  # #################

    # Add a pipe to group tokens into larger traits
    config = {'overwrite_ents': True}
    match_ruler = nlp.add_pipe('entity_ruler', name='match_ruler', config=config)
    add_ruler_patterns(match_ruler, *ENTITY_MATCHERS)

    # add_debug_pipes(nlp, 'before entity_data', entities=True)  # ###################

    nlp.add_pipe(ADD_ENTITY_DATA, config={'patterns': ENTITY_MATCHERS})

    # add_debug_pipes(nlp, 'after entity_data', entities=True)  # ####################

    config = {'patterns': [PART_LINKER, SEX_LINKER, SUBPART_LINKER]}
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
