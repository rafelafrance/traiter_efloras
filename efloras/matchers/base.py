"""Base matcher object."""

from collections import defaultdict

from traiter.matcher import Parser
from traiter.util import as_list

from ..pylib.terms import terms_from_patterns
from ..pylib.traits import MATCHER_NAMES, TRAIT2MATCHER


class Base(Parser):
    """Base matcher object."""

    def __init__(self, trait_names=None):
        super().__init__()

        # Build the traits to parse
        names = as_list(trait_names) if trait_names else list(TRAIT2MATCHER)
        names += ['plant_part']  # We always need to parse plant_parts
        self.trait_names = {k: v for k, v in TRAIT2MATCHER.items()
                            if k in sorted(names)}

        # Build the matchers we need to parse the traits
        self.matchers = {TRAIT2MATCHER[n]: MATCHER_NAMES[TRAIT2MATCHER[n]]
                         for n in names}

        # Add the parser patterns that we need
        self.patterns = {}
        for matcher in self.matchers.values():
            self.patterns = {**self.patterns, **matcher['matchers']}
        self.add_patterns(self.patterns)

        # Add the terms we need based on the patterns
        self.terms = terms_from_patterns(self.patterns)
        self.add_terms(self.terms)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        parts = []
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

            elif data:
                key = f'{category}_{label}'
                traits[key].append(data)

        if traits:
            parts.append(traits)

        print([dict(p) for p in parts])

        return parts
