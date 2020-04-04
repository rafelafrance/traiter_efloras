"""Base matcher object."""

from traiter.matcher import Matcher

import efloras.pylib.util as util
import efloras.pylib.terms as terms


class Base(Matcher):
    """Base matcher object."""

    # def __init__(self, name):
    #     super().__init__(name)

    def parse(self, text):
        """Parse the traits."""
        raise NotImplementedError

    def previous_token(self, distance, doc, start):
        """Look at the previous token with a possible dash in between."""
        if distance == 0:
            return True
        return self.dash_token(distance, doc, start)

    @staticmethod
    def dash_token(distance, doc, start):
        """Look at the previous token with a possible dash in between."""
        return distance == 1 and doc[start - 1].text in ('-',)

    def term_phrases(self, attr='lower'):
        """Get terms specific for the matcher and shared terms."""
        attr = attr.upper()

        combined = {**terms.TERMS[self.name], **terms.TERMS['shared']}
        for label, values in combined.items():
            patterns = [self.nlp.make_doc(t['term']) for t in values
                        if t['match_on'].upper() == attr]
            self.term_matcher.add(label, self.term_label, *patterns)

    def term_replace(self):
        """Get terms specific for the matcher and shared terms."""
        combined = {**terms.TERMS[self.name], **terms.TERMS['shared']}
        combined = util.flatten(list(combined.values()))
        return {t['term']: t['replace'] for t in combined if t['replace']}
