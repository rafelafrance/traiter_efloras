"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error
from traiter.util import Step  # pylint: disable=import-error

from .attach import ATTACH
from .color import COLOR
from .count import COUNT
from .descriptor import DESCRIPTOR
from .habit import HABIT
from .margin import MARGIN_SHAPE
from .part import PART
from .phrase import PHRASE
from .range import RANGE
from .shape import SHAPE
from .size import SIZE
from .suffix_count import SUFFIX_COUNT
from ..pylib.sentencizer import NLP
from ..pylib.terms import TERMS

MATCHERS = (
    COLOR, COUNT, DESCRIPTOR, HABIT, SUFFIX_COUNT, MARGIN_SHAPE, PHRASE, PART,
    SHAPE, RANGE, SIZE)


class Matcher(TraitMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    def __init__(self):
        super().__init__(NLP)

        # Process the matchers
        traiters = []
        groupers = []

        for matcher in MATCHERS:
            traiters += matcher.get('matchers', [])
            groupers += matcher.get('groupers', [])

        self.add_patterns(groupers, Step.GROUP)
        self.add_patterns(traiters, Step.TRAIT)
        self.add_patterns(ATTACH['matchers'], Step.FINAL)
        self.add_terms(TERMS)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        traits = defaultdict(list)

        for sent in doc.sents:
            augment = None

            for token in sent:
                label = token._.label
                data = {k: v for k, v in token._.data.items()
                        if not k.startswith('_')}

                # We need to consider where a plant part falls in a sentence.
                # If it is the first part in a sentence it is the "base" part
                # and we need to push any fields (like sex or location) in it
                # to all of the remaining traits & plant parts in the sentence.
                # For example:
                #   "Male flowers: petals 4-6 red."
                # Should be parsed with all traits being "male" like so:
                #   part: [{'value': 'flower', 'sex': 'male'}
                #          {'value': 'petal', 'sex': 'male'}]
                #   petal_count; [{'low': 4, 'high': 6, 'sex': 'male'}]
                #   petal_color; [{'value': 'red', 'sex':'male'}]

                if label == 'part' and augment is None:
                    augment = {k: v for k, v in data.items()
                               if k not in ('start', 'end', 'value')}

                if label and data:
                    if augment:
                        data = {**augment, **data}
                    traits[label].append(data)

        # from pprint import pp
        # pp(dict(traits))

        return traits
