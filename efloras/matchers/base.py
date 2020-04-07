"""Base matcher object."""

from spacy.matcher import Matcher, PhraseMatcher
from traiter.matcher import Matcher as TraitMatcher

import efloras.pylib.terms as terms
from ..pylib.terms import replacements


class Base(TraitMatcher):
    """Base matcher object."""

    trait_matchers = {}

    def __init__(self, name):
        super().__init__(name)
        self.term_matchers.append(PhraseMatcher(self.nlp.vocab, attr='LOWER'))
        self.literal_terms()
        self.replace = replacements(self.name)

        self.trait_matcher = Matcher(self.nlp.vocab)
        _ = [self.trait_matcher.add(k, v) for
             k, v in self.trait_matchers.items()]

    def parse(self, text):
        """Parse the traits."""
        raise NotImplementedError

    def literal_terms(self, attr='lower', index=0):
        """Get terms specific for the matcher and shared terms."""
        attr = attr.upper()

        combined = {**terms.TERMS[self.name], **terms.TERMS['shared']}
        for label, values in combined.items():
            patterns = [self.nlp.make_doc(t['term']) for t in values
                        if t['match_on'].upper() == attr]
            self.term_matchers[index].add(label, self.term_label, *patterns)

    def find_terms(self, text):
        """Find all terms in the text and return the resulting doc.

        There may be more than one matcher for the terms. Gather the results
        for each one and combine them. Then retokenize the doc to handle terms
        that span multiple tokens.
        """
        doc = self.nlp(text)

        matches = []
        for matcher in self.term_matchers:
            matches += matcher(doc)
        matches = self.leftmost_longest(matches)

        with doc.retokenize() as retokenizer:
            for match_id, start, end in matches:
                retokenizer.merge(doc[start:end])

        return doc

    def get_trait_matches(self, doc):
        """Get the trait matches."""
        matches = self.trait_matcher(doc)
        if not matches:
            return []
        return self.leftmost_longest(matches)
