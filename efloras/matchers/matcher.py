"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher

from ..pylib.terms import terms_from_patterns
from ..pylib.traits import expand_trait_names, traits_to_matchers


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self, trait_names=None):
        super().__init__()

        self.trait_names = expand_trait_names(trait_names)
        matchers = traits_to_matchers(self.trait_names)

        # Process the matchers
        trait_patterns = {}
        group_patterns = {}
        aux_names = []

        for matcher in matchers:
            trait_patterns = {**trait_patterns, **matcher['matchers']}
            group_patterns = {**group_patterns, **matcher.get('groupers', {})}
            aux_names += matcher.get('aux_names', [])

        self.add_trait_patterns(trait_patterns)
        self.add_group_patterns(group_patterns)

        self.trait_filter = set(self.trait_names + aux_names)

        # We can now add the terms
        patterns = [p['patterns'] for p in trait_patterns.values()]
        self.terms = terms_from_patterns(patterns)
        self.terms += terms_from_patterns(group_patterns)
        self.add_terms(self.terms)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        parts = []
        descriptors = defaultdict(list)
        traits = defaultdict(list)

        category = ''

        for token in doc:
            label = token._.label
            data = token._.data

            if label == 'part':
                if traits:
                    parts.append(traits)
                category = data['value']
                traits = defaultdict(list)
                traits[label].append(data)

            elif label == 'descriptor' and data:
                trait_name = data['category']
                if trait_name in self.trait_filter:
                    del data['category']
                    descriptors[trait_name].append(data)

            elif data:
                trait_name = f'{category}_{label}'
                if trait_name in self.trait_filter:
                    traits[trait_name].append(data)

        if traits:
            parts.append(traits)

        if descriptors:
            parts = [descriptors] + parts

        # print()
        # from pprint import pp
        # pp([dict(p) for p in parts])

        return parts
