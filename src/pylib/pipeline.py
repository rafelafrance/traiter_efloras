"""Create a trait pipeline."""

import spacy
from traiter.sentencizer import Sentencizer
from traiter.spacy_nlp import setup_tokenizer
from traiter.trait_pipeline import TraitPipeline

from .util import ABBREVS, LINK_STEP, TRAIT_STEP
from ..matchers.link_matcher import LinkMatcher
from ..matchers.matcher import Matcher


class Pipeline(TraitPipeline):
    """Build a custom traiter pipeline."""

    steps2link = {TRAIT_STEP, LINK_STEP}

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        super().__init__(self.nlp)

        self.nlp.disable_pipes(['ner'])

        setup_tokenizer(self.nlp)

        matcher = Matcher(self.nlp)
        linker = LinkMatcher(self.nlp)

        sentencizer = Sentencizer(ABBREVS)

        self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(matcher, last=True)
        self.nlp.add_pipe(linker, last=True, name=LINK_STEP)


PIPELINE = Pipeline()
