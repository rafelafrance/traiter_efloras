"""Common logic for parsing trait notations."""
from traiter.new.nlp import spacy_nlp
from traiter.new.matcher import get_matches


class Base:
    """Shared lexer logic."""

    def __init__(self, name, patterns):
        self.name = name
        self.patterns = patterns
        self.nlp = spacy_nlp(self)

    def __call__(self, doc):
        """Do the actual pattern matching here."""
        matches = get_matches(self.patterns, doc)

        for token in doc:
            print(token)
        print()

        for match in matches:
            print(match.pattern_idx, match.token_start, match.token_end)
            print(doc[match.token_start:match.token_end])

        return doc

    def parse(self, text):
        """Parse the document."""

        doc = self.nlp(text)

        for trait in doc._.traits:
            print(trait)

        return doc._.traits
