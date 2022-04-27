"""Create a trait pipeline."""
import spacy
from traiter import tokenizer_util
from traiter.patterns import matcher_patterns
from traiter.pipes.add_traits_pipe import ADD_TRAITS
from traiter.pipes.delete_traits_pipe import DELETE_TRAITS
from traiter.pipes.dependency_pipe import DEPENDENCY
from traiter.pipes.sentence_pipe import SENTENCE
from traiter.pipes.simple_traits_pipe import SIMPLE_TRAITS
from traiter.pipes.term_pipe import TERM_PIPE

from efloras.patterns import color
from efloras.patterns import count
from efloras.patterns import location_linker
from efloras.patterns import margin
from efloras.patterns import part_linker
from efloras.patterns import part_location
from efloras.patterns import range_
from efloras.patterns import sex_linker
from efloras.patterns import shape
from efloras.patterns import size
from efloras.patterns import subpart_linker
from efloras.pylib import const

# from traiter.pipes.debug import DEBUG_TOKENS, DEBUG_ENTITIES


def pipeline():
    """Create a pipeline for extracting traits."""
    nlp = spacy.load("en_core_web_sm", exclude=["ner"])
    tokenizer_util.append_tokenizer_regexes(nlp)
    tokenizer_util.append_abbrevs(nlp, const.ABBREVS)

    nlp.add_pipe(
        TERM_PIPE,
        before="parser",
        config={
            "terms": const.TERMS.terms,
            "replace": const.REPLACE,
        },
    )

    nlp.add_pipe(SENTENCE, before="parser")

    nlp.add_pipe(
        ADD_TRAITS,
        name="range_pipe",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
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
            )
        },
    )
    nlp.add_pipe("merge_entities")

    nlp.add_pipe(SIMPLE_TRAITS, config={"replace": const.REPLACE})

    nlp.add_pipe(
        ADD_TRAITS,
        name="numeric_traits",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    size.SIZE,
                    size.SIZE_HIGH_ONLY,
                    size.SIZE_DOUBLE_DIM,
                    size.NOT_A_SIZE,
                    count.COUNT,
                    count.COUNT_WORD,
                    count.NOT_A_COUNT,
                    color.COLOR,
                    margin.MARGIN_SHAPE,
                    shape.N_SHAPE,
                    shape.SHAPE,
                    part_location.PART_AS_LOCATION,
                    part_location.SUBPART_AS_LOCATION,
                ]
            )
        },
    )

    nlp.add_pipe(DELETE_TRAITS, config={"delete": const.FORGET})

    # nlp.add_pipe(DEBUG_TOKENS, config={'message': ''})
    # nlp.add_pipe(DEBUG_ENTITIES, config={'message': ''})

    nlp.add_pipe(
        DEPENDENCY,
        name="part_linker",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    location_linker.LOCATION_LINKER,
                    part_linker.PART_LINKER,
                    sex_linker.SEX_LINKER,
                    subpart_linker.SUBPART_LINKER,
                ]
            )
        },
    )

    return nlp
