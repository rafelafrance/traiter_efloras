"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from .all_matchers import MATCHERS
from ..pylib.attach_fsm import attach_traits_to_parts
from ..pylib.sentencizer import NLP
from ..pylib.terms import TERMS
from ..pylib.util import ATTACH_STEPS, FINAL_STEP, GROUP_STEP, TRAIT_STEP


class Matcher(TraitMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    def __init__(self, attach=True):
        super().__init__(NLP)

        self.attach = attach

        self.add_terms(TERMS)

        traiters = []
        groupers = []
        attachers = []

        for matcher in MATCHERS:
            traiters += matcher.get('traits', [])
            groupers += matcher.get('groupers', [])
            attachers += matcher.get('attachers', [])

        self.add_patterns(groupers, GROUP_STEP)
        self.add_patterns(traiters, TRAIT_STEP)
        self.add_patterns(attachers, FINAL_STEP)

    def parse(self, text, with_sents=False):
        """Parse the traits."""
        doc = super().parse(text)

        traits = defaultdict(list)

        sents = []

        for sent in doc.sents:
            sents.append((sent.start_char, sent.end_char))

            if self.attach:
                attach_traits_to_parts(sent)

            for token in sent:
                if (token._.step in ATTACH_STEPS and token._.data
                        and not token._.aux.get('skip')):
                    data = {k: v for k, v in token._.data.items()
                            if not k.startswith('_')}
                    data['start'] = token.idx
                    data['end'] = token.idx + len(token)
                    traits[token._.label].append(data)

        # from pprint import pp
        # pp(dict(traits))

        # TODO: FIXME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return (traits, sents) if with_sents else traits
