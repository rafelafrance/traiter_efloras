"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error
from traiter.util import Step  # pylint: disable=import-error

from .all_matchers import MATCHERS
from ..pylib.attach import attach_traits_to_parts
from ..pylib.sentencizer import NLP
from ..pylib.terms import TERMS


class Matcher(TraitMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    def __init__(self):
        super().__init__(NLP)

        traiters = []
        groupers = []

        for matcher in MATCHERS:
            traiters += matcher.get('matchers', [])
            groupers += matcher.get('groupers', [])

        self.add_patterns(groupers, Step.GROUP)
        self.add_patterns(traiters, Step.TRAIT)
        self.add_terms(TERMS)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        for sent in doc.sents:
            attach_traits_to_parts(sent)

        traits = defaultdict(list)
        for token in doc:
            if token._.step == Step.TRAIT and token._.data:
                data = {k: v for k, v in token._.data.items()
                        if not k.startswith('_')}
                data['start'] = token.idx
                data['end'] = token.idx + len(token)
                traits[token._.label].append(data)

        from pprint import pp
        pp(dict(traits))

        return traits
