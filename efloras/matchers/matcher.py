"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from .plant_color import PLANT_COLOR
from .plant_count import PLANT_COUNT
from .plant_descriptor import PLANT_DESCRIPTOR
from .plant_part import PLANT_PART
from .plant_shape import PLANT_SHAPE
from .plant_size import PLANT_SIZE
from ..pylib.customize_pipeline import NLP
from ..pylib.terms import TERMS

MATCHERS = [PLANT_COLOR, PLANT_COUNT, PLANT_DESCRIPTOR, PLANT_PART,
            PLANT_SHAPE, PLANT_SIZE]


class Matcher(TraitMatcher):
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
        self.add_terms(TERMS)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        parts = []
        descriptors = defaultdict(list)
        traits = defaultdict(list)

        for sent in doc.sents:
            part = ''
            augment = {}

            for token in sent:
                label = token._.label
                data = token._.data

                if label == 'part':
                    if traits:
                        parts.append(traits)
                    part = data['value']
                    traits = defaultdict(list)
                    if not augment:
                        augment = {k: v for k, v in data.items()
                                   if k not in ('start', 'end', 'value')}
                    for k, v in augment.items():
                        if k not in data:
                            data[k] = v
                    traits['part'].append(data)

                elif label == 'descriptor' and data.get('category'):
                    name = data['category']
                    del data['category']
                    descriptors[name].append(data)

                elif data and part:
                    label = f'{part}_{label}'
                    for k, v in augment.items():
                        if k not in data:
                            data[k] = v
                    traits[label].append(data)

        if traits:
            parts.append(traits)

        if descriptors:
            parts = [descriptors] + parts

        # from pprint import pp
        # pp([dict(p) for p in parts])

        return parts
