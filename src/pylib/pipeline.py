"""Create a trait pipeline."""

# pylint: disable=import-error
from traiter.spacy_nlp.pipeline import SpacyPipeline
from traiter.spacy_nlp.sentencizer import SpacySentencizer

from .util import ABBREVS, LINK_STEP, TRAIT_STEP
from ..matchers.link_matcher import LinkMatcher
from ..matchers.matcher import Matcher


class Pipeline(SpacyPipeline):  # pylint: disable=too-few-public-methods
    """Build a custom traiter pipeline."""

    steps2link = {TRAIT_STEP, LINK_STEP}

    def __init__(self, gpu='prefer', training=False):
        super().__init__(gpu=gpu)

        self.nlp.disable_pipes(['ner'])

        sentencizer = SpacySentencizer(ABBREVS)
        self.nlp.add_pipe(sentencizer, before='parser')

        matcher = Matcher(self.nlp, training=training)
        self.nlp.add_pipe(matcher, last=True, name=TRAIT_STEP)

        linker = LinkMatcher(self.nlp)
        self.nlp.add_pipe(linker, last=True, name=LINK_STEP)


PIPELINE = Pipeline()
