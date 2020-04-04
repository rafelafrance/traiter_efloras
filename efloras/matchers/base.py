"""Base matcher object."""

from traiter.matcher import Matcher

import efloras.pylib.util as util
import efloras.pylib.terms as terms


class Base(Matcher):
    """Base matcher object."""

    def parse(self, text):
        """Parse the traits."""
        raise NotImplementedError

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
