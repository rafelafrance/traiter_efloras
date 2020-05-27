"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from ..pylib.terms import TERMS
from .plant_color import PLANT_COLOR
from .plant_count import PLANT_COUNT
from .plant_descriptor import PLANT_DESCRIPTOR
from .plant_part import PLANT_PART
from .plant_shape import PLANT_SHAPE
from .plant_size import PLANT_SIZE

MATCHERS = [PLANT_COLOR, PLANT_COUNT, PLANT_DESCRIPTOR, PLANT_PART,
            PLANT_SHAPE, PLANT_SIZE]


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self):
        super().__init__()

        # Process the matchers
        trait_patterns = []
        group_patterns = {}

        for matcher in MATCHERS:
            trait_patterns += matcher['matchers']
            group_patterns = {**group_patterns, **matcher.get('groupers', {})}

        self.add_trait_patterns(trait_patterns)
        self.add_group_patterns(group_patterns)
        self.add_terms(TERMS)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        parts = []
        descriptors = defaultdict(list)
        traits = defaultdict(list)

        part = ''

        for token in doc:
            label = token._.label
            data = token._.data

            if label == 'part':
                if traits:
                    parts.append(traits)
                label = 'part'
                part = data['value']
                traits = defaultdict(list)
                traits[label].append(data)

            elif label == 'descriptor' and data.get('category'):
                name = data['category']
                del data['category']
                descriptors[name].append(data)

            elif data and part:
                label = f'{part}_{label}'
                traits[label].append(data)

        if traits:
            parts.append(traits)

        if descriptors:
            parts = [descriptors] + parts

        # from pprint import pp
        # pp([dict(p) for p in parts])

        return parts
