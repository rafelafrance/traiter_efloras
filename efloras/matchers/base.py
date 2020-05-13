"""Base matcher object."""

from spacy.matcher import Matcher
from traiter.catalog import CODE_LEN
from traiter.matcher import Parser

from ..pylib.catalog import CATALOG


class Base(Parser):
    """Base matcher object."""

    term_list = []
    trait_matchers = {}
    raw_groupers = {}
    raw_producers = []

    def __init__(self, name):
        super().__init__(name, CATALOG)

        self.groupers = self.build_groupers()
        self.producers = self.build_producers()
        self.build_spacy_matchers()

        self.replace = CATALOG.get_term_replacements(self.term_list)

        # TODO: Delete this
        self.trait_matcher = Matcher(self.nlp.vocab)
        _ = [self.trait_matcher.add(k, v) for
             k, v in self.trait_matchers.items()]

    def get_trait_matches(self, doc):
        """Get the trait matches."""
        # TODO: Delete this
        matches = self.trait_matcher(doc)
        if not matches:
            return []
        return self.leftmost_longest(matches)

    def find_terms(self, text):
        """Find all terms in the text and return the resulting doc.

        There may be more than one matcher for the terms. Gather the results
        for each one and combine them. Then retokenize the doc to handle terms
        that span multiple tokens.
        """
        doc = self.nlp(text)

        matches = []

        for matcher in self.matchers.values():
            matches += matcher(doc)

        matches = self.leftmost_longest(matches)

        with doc.retokenize() as retokenizer:
            for match_id, start, end in matches:
                retokenizer.merge(doc[start:end])

        return doc

    def parse(self, text):
        """Parse the traits."""
        doc = self.find_terms(text)

        # Because we elide over some tokens we need an easy way to map them
        token_map = [t.i for t in doc if t._.code]

        encoded = [t._.code for t in doc if t._.code]
        encoded = ''.join(encoded)

        enriched_matches = []
        for func, regexp in self.producers:
            for match in regexp.finditer(encoded):
                start, end = match.span()
                enriched_matches.append((func, start, end, match))

        enriched_matches = self.leftmost_longest(enriched_matches)

        all_traits = []
        for enriched_match in enriched_matches:
            action, _, _, match = enriched_match

            traits = action(self, doc, match, token_map)

            if not traits:
                continue

            all_traits += traits if isinstance(traits, list) else [traits]

            return all_traits


def group2span(doc, match, group, token_map):
    """Convert a regex match group into a spacy span."""
    start = match.start(group) // CODE_LEN
    start = token_map[start]
    end = match.end(group) // CODE_LEN
    end = token_map[end-1] + 1
    return doc[start:end]
