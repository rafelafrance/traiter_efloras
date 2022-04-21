"""Create a trait pipeline."""

import spacy
from traiter.patterns import matcher_patterns
from traiter.old_pipes.add_entity_data import ADD_ENTITY_DATA
from traiter.old_pipes.cleanup import CLEANUP
from traiter.old_pipes.dependency import DEPENDENCY
from traiter.old_pipes.sentence import SENTENCE
from traiter.old_pipes.simple_entity_data import SIMPLE_ENTITY_DATA
from traiter.old_pipes.update_entity_data import UPDATE_ENTITY_DATA
from traiter.tokenizer_util import append_abbrevs, append_tokenizer_regexes

from efloras.patterns import (
    color, count, location_linker, margin, part_linker,
    part_location, range_, sex_linker, shape, size, subpart_linker,
)
from efloras.pylib import const

# from traiter.pipes.debug import DEBUG_TOKENS, DEBUG_ENTITIES

TERM_RULES = [
    range_.RANGE_LOW,
    range_.RANGE_MIN_LOW,
    range_.RANGE_LOW_HIGH,
    range_.RANGE_LOW_MAX,
    range_.RANGE_MIN_LOW_HIGH,
    range_.RANGE_MIN_LOW_MAX,
    range_.RANGE_LOW_HIGH_MAX,
    range_.RANGE_MIN_LOW_HIGH_MAX,
    range_.NOT_A_RANGE,
]

ADD_DATA = [
    color.COLOR,
    margin.MARGIN_SHAPE,
    shape.N_SHAPE,
    shape.SHAPE,
    part_location.PART_AS_LOCATION,
    part_location.SUBPART_AS_LOCATION,
]

UPDATE_DATA = [
    count.COUNT,
    count.COUNT_WORD,
    count.NOT_A_COUNT,
    size.SIZE,
    size.SIZE_HIGH_ONLY,
    size.SIZE_DOUBLE_DIM,
    size.NOT_A_SIZE]

LINKERS = [
    location_linker.LOCATION_LINKER,
    part_linker.PART_LINKER,
    sex_linker.SEX_LINKER,
    subpart_linker.SUBPART_LINKER,
]


def pipeline():
    """Create a pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner'])
    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, const.ABBREVS)

    # Add a pipe to identify phrases and patterns as base-level traits.
    term_ruler = nlp.add_pipe(
        'entity_ruler',
        name='term_ruler',
        before='parser',
        config={'phrase_matcher_attr': 'LOWER'}
    )
    term_ruler.add_patterns(const.TERMS.for_entity_ruler())
    matcher_patterns.add_ruler_patterns(term_ruler, TERM_RULES)

    nlp.add_pipe(SENTENCE, before='parser')

    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe(
        SIMPLE_ENTITY_DATA,
        after='term_merger',
        config={'replace': const.REPLACE},
    )

    config = {'patterns': matcher_patterns.as_dicts(UPDATE_DATA)}
    nlp.add_pipe(UPDATE_ENTITY_DATA, name='update_entities', config=config)

    # Add a pipe to group tokens into larger traits
    config = {'overwrite_ents': True}
    match_ruler = nlp.add_pipe('entity_ruler', name='match_ruler', config=config)
    matcher_patterns.add_ruler_patterns(match_ruler, ADD_DATA)

    nlp.add_pipe(
        ADD_ENTITY_DATA,
        config={'dispatch': matcher_patterns.patterns_to_dispatch(ADD_DATA)},
    )

    nlp.add_pipe(CLEANUP, config={'forget': const.FORGET})

    # nlp.add_pipe(DEBUG_TOKENS, config={'message': ''})
    # nlp.add_pipe(DEBUG_ENTITIES, config={'message': ''})

    config = {'patterns': matcher_patterns.as_dicts(LINKERS)}
    nlp.add_pipe(DEPENDENCY, name='part_linker', config=config)

    return nlp
