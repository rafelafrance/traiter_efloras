"""Create a trait pipeline."""

import spacy
from traiter.patterns.matcher_patterns import (
    add_ruler_patterns, as_dicts, patterns_to_dispatch)
from traiter.pipes.add_entity_data import ADD_ENTITY_DATA
from traiter.pipes.cleanup import CLEANUP
from traiter.pipes.dependency import DEPENDENCY
from traiter.pipes.sentence import SENTENCE
from traiter.pipes.simple_entity_data import SIMPLE_ENTITY_DATA
from traiter.pipes.update_entity_data import UPDATE_ENTITY_DATA
from traiter.tokenizer_util import append_abbrevs, append_tokenizer_regexes

from efloras.patterns.color import COLOR
from efloras.patterns.count import COUNT, COUNT_WORD, NOT_A_COUNT
from efloras.patterns.location_linker import LOCATION_LINKER
from efloras.patterns.margin import MARGIN_SHAPE
from efloras.patterns.part_linker import PART_LINKER
from efloras.patterns.part_location import PART_AS_LOCATION, SUBPART_AS_LOCATION
from efloras.patterns.range import (
    NOT_A_RANGE, RANGE_LOW, RANGE_LOW_HIGH, RANGE_LOW_HIGH_MAX, RANGE_LOW_MAX,
    RANGE_MIN_LOW, RANGE_MIN_LOW_HIGH, RANGE_MIN_LOW_HIGH_MAX, RANGE_MIN_LOW_MAX)
from efloras.patterns.sex_linker import SEX_LINKER
from efloras.patterns.shape import N_SHAPE, SHAPE
from efloras.patterns.size import NOT_A_SIZE, SIZE, SIZE_DOUBLE_DIM, SIZE_HIGH_ONLY
from efloras.patterns.subpart_linker import SUBPART_LINKER
from efloras.pylib.const import ABBREVS, FORGET, REPLACE, TERMS

# from traiter.pipes.debug import DEBUG_ENTITIES, DEBUG_TOKENS

TERM_RULES = [
    RANGE_LOW, RANGE_MIN_LOW, RANGE_LOW_HIGH, RANGE_LOW_MAX, RANGE_MIN_LOW_HIGH,
    RANGE_MIN_LOW_MAX, RANGE_LOW_HIGH_MAX, RANGE_MIN_LOW_HIGH_MAX, NOT_A_RANGE]

ADD_DATA = [
    COLOR, MARGIN_SHAPE, N_SHAPE, SHAPE, PART_AS_LOCATION, SUBPART_AS_LOCATION]

UPDATE_DATA = [
    COUNT, COUNT_WORD, NOT_A_COUNT, SIZE, SIZE_HIGH_ONLY, SIZE_DOUBLE_DIM, NOT_A_SIZE]

LINKERS = [LOCATION_LINKER, PART_LINKER, SEX_LINKER, SUBPART_LINKER]


def pipeline():
    """Create a pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner'])
    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, ABBREVS)

    # Add a pipe to identify phrases and patterns as base-level traits.
    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe(
        'entity_ruler', name='term_ruler', config=config, before='parser')
    term_ruler.add_patterns(TERMS.for_entity_ruler())
    add_ruler_patterns(term_ruler, TERM_RULES)

    nlp.add_pipe(SENTENCE, before='parser')

    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe(SIMPLE_ENTITY_DATA, after='term_merger', config={'replace': REPLACE})

    config = {'patterns': as_dicts(UPDATE_DATA)}
    nlp.add_pipe(UPDATE_ENTITY_DATA, name='update_entities', config=config)

    # Add a pipe to group tokens into larger traits
    config = {'overwrite_ents': True}
    match_ruler = nlp.add_pipe('entity_ruler', name='match_ruler', config=config)
    add_ruler_patterns(match_ruler, ADD_DATA)

    nlp.add_pipe(ADD_ENTITY_DATA, config={'dispatch': patterns_to_dispatch(ADD_DATA)})

    nlp.add_pipe(CLEANUP, config={'forget': FORGET})

    # nlp.add_pipe(DEBUG_TOKENS, config={'message': ''})
    # nlp.add_pipe(DEBUG_ENTITIES, config={'message': ''})

    config = {'patterns': as_dicts(LINKERS)}
    nlp.add_pipe(DEPENDENCY, name='part_linker', config=config)

    return nlp
