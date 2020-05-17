"""Base matcher object."""

from traiter.matcher import Parser
from traiter.util import as_list, DotDict as Trait


from ..pylib.terms import terms4patterns
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
        self.terms = terms4patterns(self.patterns)
        self.add_terms(self.terms)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        traits = []

        trait = Trait(end=0, start=len(text), value=[])

        value = {}

        for token in doc:
            trait_name = token._.trait
            data = token._.data
            if trait_name == 'plant_part':
                trait.part = data['part']
            elif trait_name in self.matchers:
                trait.start = min(token.idx, trait.start)
                trait.end = max(token.idx + len(token), trait.end)
                for val in data['value']:
                    value[val] = 1
        trait.value = list(value)
        trait.raw_value = text[trait.start:trait.end]

        traits.append(trait)

        return traits
