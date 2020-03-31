"""Common logic for parsing trait notations."""
from traiter.new.nlp import spacy_nlp


class Base:  # pylint: disable=too-few-public-methods
    """Shared lexer logic."""

    def __init__(self, name, patterns):
        self.name = name
        self.patterns = patterns
        self.nlp = spacy_nlp(self.patterns)

    def extract(self, text):
        """Find the traits in the text."""
        all_traits = []
        print(text)

        for token in self.nlp(text):
            print(token.text, token.lemma_, token._.canon, token.pos_)

        print()

        # tokens = super().parse(text)
        #
        # for token in tokens:
        #
        #     traits = token.action(token)
        #
        #     # The action function may reject the token
        #     if not traits:
        #         continue
        #
        #     all_traits += traits if isinstance(traits, list) else [traits]

        return all_traits
