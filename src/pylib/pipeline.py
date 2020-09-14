"""Create a trait pipeline."""

# pylint: disable=import-error
from traiter.sentencizer import Sentencizer
from traiter.spacy_nlp import setup_tokenizer, spacy_nlp
from traiter.trait_pipeline import TraitPipeline

from .util import ABBREVS, LINK_STEP, TRAIT_STEP
from ..matchers.link_matcher import LinkMatcher
from ..matchers.matcher import Matcher


class Pipeline(TraitPipeline):  # pylint: disable=too-few-public-methods
    """Build a custom traiter pipeline."""

    steps2link = {TRAIT_STEP, LINK_STEP}

    def __init__(self, gpu='prefer', training=False):
        self.nlp = spacy_nlp(gpu=gpu)
        super().__init__(self.nlp)

        self.nlp.disable_pipes(['ner'])

        setup_tokenizer(self.nlp)

        sentencizer = Sentencizer(ABBREVS)
        self.nlp.add_pipe(sentencizer, before='parser')

        matcher = Matcher(self.nlp, training=training)
        self.nlp.add_pipe(matcher, last=True, name=TRAIT_STEP)

        linker = LinkMatcher(self.nlp)
        self.nlp.add_pipe(linker, last=True, name=LINK_STEP)


PIPELINE = Pipeline()
