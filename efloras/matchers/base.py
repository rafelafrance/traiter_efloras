"""Base matcher object."""

from traiter.catalog import Catalog
from traiter.matcher import Parser
from traiter.pattern import CODE_LEN, Type

import efloras.pylib.util as util

CATALOG = Catalog()
CATALOG.read_terms(util.DATA_DIR / 'terms.csv')


class Base(Parser):
    """Base matcher object."""

    def __init__(self, name):
        super().__init__(name, CATALOG)
        # self.replace = CATALOG.get_term_replacements()

    def get_term_replacements(self):
        """Get replacement values for a term."""
        return {t['term']: r for p in self.patterns[Type.PHRASE]
                for t in p.terms if (r := t.get('replace'))}


def group2span(doc, match, group, token_map):
    """Convert a regex match group into a spacy span."""
    start = match.start(group) // CODE_LEN
    start = token_map[start]
    end = match.end(group) // CODE_LEN
    end = token_map[end-1] + 1
    return doc[start:end]
