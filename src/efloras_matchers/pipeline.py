"""Create a trait pipeline."""

# pylint: disable=import-error
from traiter.spacy_nlp.pipeline import SpacyPipeline
from traiter.spacy_nlp.sentencizer import SpacySentencizer

from .link_matcher import LinkMatcher
from .matcher import Matcher
from ..pylib.util import ABBREVS, LINK_STEP, TRAIT_STEP


class Pipeline(SpacyPipeline):  # pylint: disable=too-few-public-methods
    """Build a custom traiter pipeline."""

    token2entity = {TRAIT_STEP, LINK_STEP}

    def __init__(
            self,
            gpu: str = 'prefer',
            training: bool = False,
            tokenizer: bool = True
    ) -> None:
        super().__init__(gpu=gpu, tokenizer=tokenizer)

        self.nlp.disable_pipes(['ner'])

        matcher = Matcher(self.nlp, training=training)
        self.nlp.add_pipe(matcher, last=True, name=TRAIT_STEP)

        if not training:
            sentencizer = SpacySentencizer(ABBREVS)
            self.nlp.add_pipe(sentencizer, before='parser')

            linker = LinkMatcher(self.nlp)
            self.nlp.add_pipe(linker, last=True, name=LINK_STEP)


PIPELINE = Pipeline()  # A singleton for testing
