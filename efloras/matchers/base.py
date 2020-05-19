"""Base matcher object."""

from collections import defaultdict

from traiter.matcher import Parser

from ..pylib.terms import terms_from_patterns
from ..pylib.traits import expand_trait_names, traits_to_matchers


class Base(Parser):
    """Base matcher object."""

    def __init__(self, trait_names=None):
        super().__init__()

        self.trait_names = expand_trait_names(trait_names)
        matchers = traits_to_matchers(self.trait_names)

        # Get what we need from the matchers
        patterns = {}
        aux_names = []
        for matcher in matchers:
            patterns = {**patterns, **matcher['matchers']}
            aux_names += matcher.get('aux_names', [])
        self.add_patterns(patterns)
        self.trait_filter = set(self.trait_names + aux_names)

        self.terms = terms_from_patterns(patterns)
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
                trait_name = f'{data["category"]}'
                if trait_name in self.trait_filter:
                    descriptors[trait_name].append(data)

            elif data:
                trait_name = f'{category}_{label}'
                if trait_name in self.trait_filter:
                    traits[trait_name].append(data)

        if traits:
            parts.append(traits)

        if descriptors:
            parts = [descriptors] + parts

        print()
        from pprint import pp
        pp([dict(p) for p in parts])
        print()

        return parts
