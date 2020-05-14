"""Base matcher object."""

from spacy.matcher import Matcher
from traiter.pattern import CODE_LEN
from traiter.matcher import Parser

from ..pylib.catalog import CATALOG


class Base(Parser):
    """Base matcher object."""

    def __init__(self, name):
        super().__init__(name, CATALOG)
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


def group2span(doc, match, group, token_map):
    """Convert a regex match group into a spacy span."""
    start = match.start(group) // CODE_LEN
    start = token_map[start]
    end = match.end(group) // CODE_LEN
    end = token_map[end-1] + 1
    return doc[start:end]
