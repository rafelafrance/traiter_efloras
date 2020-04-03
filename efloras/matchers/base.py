"""Base matcher object."""

from traiter.matcher import Matcher


class Base(Matcher):
    """Base matcher object."""

    def parse(self, text):
        """Parse the traits."""
        raise NotImplementedError

    @staticmethod
    def previous_token(distance, doc, start):
        """Look at the previous token with a possible dash in between."""
        if distance == 0:
            return True
        return distance == 1 and doc[start-1].text in ('-',)
