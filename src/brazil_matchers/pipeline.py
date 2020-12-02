"""Create a trait pipeline."""

# pylint: disable=import-error
from traiter.pylib.pipeline import SpacyPipeline
from traiter.pylib.sentencizer import SpacySentencizer
from traiter.pylib.to_entities import ToEntities

from .attach import attach
from .matcher import Matcher
from ..pylib.util import ABBREVS, GROUP_STEP, LINK_STEP, TRAIT_STEP


class Pipeline(SpacyPipeline):  # pylint: disable=too-few-public-methods
    """Build a custom traiter pipeline."""

    token2entity = {TRAIT_STEP, LINK_STEP, GROUP_STEP}

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

            to_entities = ToEntities(token2entity=self.token2entity)
            self.nlp.add_pipe(to_entities, last=True)

            self.nlp.add_pipe(attach, last=True, name=LINK_STEP)
