"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from .attach import ATTACH
from .color import COLOR
from .count import COUNT
from .descriptor import DESCRIPTOR
from .habit import HABIT
from .margin import MARGIN_SHAPE
from .part import PART
from .phrase import PHRASE
from .shape import SHAPE
from .size import SIZE
from ..pylib.sentencizer import NLP
from ..pylib.terms import TERMS

MATCHERS = (
    COLOR, COUNT, DESCRIPTOR, HABIT, MARGIN_SHAPE, PHRASE, PART, SHAPE, SIZE)


class Matcher(TraitMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    def __init__(self):
        super().__init__(NLP)

        # Process the matchers
        trait_patterns = []
        group_patterns = {}

        for matcher in MATCHERS:
            trait_patterns += matcher['matchers']
            group_patterns = {**group_patterns, **matcher.get('groupers', {})}

        self.add_trait_patterns(trait_patterns)
        self.add_group_patterns(group_patterns)

        self.add_final_patterns(ATTACH['matchers'])

        self.add_terms(TERMS)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        traits = defaultdict(list)

        for sent in doc.sents:
            augment = None

            for token in sent:
                label = token._.label
                data = token._.data

                # For plant parts we need to consider where a part falls
                # in a sentence. If it is the first part in a sentence it
                # is the "base" part and we need to push any fields (like
                # sex or location) in it to all of the remaining traits &
                # plant parts in the sentence. For example:
                #   "Male flowers: petals 4-6 red"
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
