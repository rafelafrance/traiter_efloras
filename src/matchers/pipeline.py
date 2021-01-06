"""Create a trait pipeline."""

# pylint: disable=import-error
from traiter.pylib.pipeline import SpacyPipeline
from traiter.pylib.sentencizer import SpacySentencizer
from traiter.pylib.to_entities import ToEntities

from .link_matcher import LinkMatcher
from .matcher import Matcher
from ..pylib.consts import ABBREVS, LINK_STEP, TRAIT_STEP


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

            to_entities = ToEntities(token2entity=self.token2entity)
            self.nlp.add_pipe(to_entities, last=True)
