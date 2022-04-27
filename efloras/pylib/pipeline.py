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

from ..patterns import color_patterns
from ..patterns import count_patterns
from ..patterns import location_linker_patterns
from ..patterns import margin_patterns
from ..patterns import part_linker_patterns
from ..patterns import part_location_patterns
from ..patterns import range_patterns
from ..patterns import sex_linker_patterns
from ..patterns import shape_patterns
from ..patterns import size_patterns
from ..patterns import subpart_linker_patterns
from ..pylib import const

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
                    range_patterns.RANGE_LOW,
                    range_patterns.RANGE_MIN_LOW,
                    range_patterns.RANGE_LOW_HIGH,
                    range_patterns.RANGE_LOW_MAX,
                    range_patterns.RANGE_MIN_LOW_HIGH,
                    range_patterns.RANGE_MIN_LOW_MAX,
                    range_patterns.RANGE_LOW_HIGH_MAX,
                    range_patterns.RANGE_MIN_LOW_HIGH_MAX,
                    range_patterns.NOT_A_RANGE,
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
                    size_patterns.SIZE,
                    size_patterns.SIZE_HIGH_ONLY,
                    size_patterns.SIZE_DOUBLE_DIM,
                    size_patterns.NOT_A_SIZE,
                    count_patterns.COUNT,
                    count_patterns.COUNT_WORD,
                    count_patterns.NOT_A_COUNT,
                    color_patterns.COLOR,
                    margin_patterns.MARGIN_SHAPE,
                    shape_patterns.N_SHAPE,
                    shape_patterns.SHAPE,
                    part_location_patterns.PART_AS_LOCATION,
                    part_location_patterns.SUBPART_AS_LOCATION,
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
                    location_linker_patterns.LOCATION_LINKER,
                    part_linker_patterns.PART_LINKER,
                    sex_linker_patterns.SEX_LINKER,
                    subpart_linker_patterns.SUBPART_LINKER,
                ]
            )
        },
    )

    return nlp
