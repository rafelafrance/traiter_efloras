"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from ..pylib.terms import terms_from_patterns
from ..pylib.traits import expand_trait_names, traits_to_matchers


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self, trait_names=None):
        super().__init__()

        self.trait_names = expand_trait_names(trait_names)
        matchers = traits_to_matchers(self.trait_names)

        # Process the matchers
        trait_patterns = []
        group_patterns = {}
        aux_names = set()

        for matcher in matchers:
            trait_patterns += matcher['matchers']
            group_patterns = {**group_patterns, **matcher.get('groupers', {})}
            aux_names |= set(matcher.get('aux_names', []))

        self.add_trait_patterns(trait_patterns)
        self.add_group_patterns(group_patterns)

        self.trait_filter = set(self.trait_names | aux_names)

        # We can now add the terms
        patterns = [p['patterns'] for p in trait_patterns]
        self.terms = terms_from_patterns(patterns)
        self.terms += terms_from_patterns(group_patterns)
        self.add_terms(self.terms)

    def parse(self, text, part='plant'):
        """Parse the traits."""
        doc = super().parse(text)
        traits = defaultdict(list)

        for token in doc:
            label = token._.label
            data = token._.data

            if label == 'descriptor':
                label = data.get('category')
                del data['category']
            else:
                label = f'{part}_{label}'

            if data:
                traits[label].append(data)

        # from pprint import pp
        # print()
        # pp(dict(traits))

        return traits if traits else {}
