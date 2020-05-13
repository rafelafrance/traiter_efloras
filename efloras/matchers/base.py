"""Base matcher object."""

import regex
from spacy.matcher import Matcher, PhraseMatcher
from traiter.matcher import Matcher as TraitMatcher, CODES, CODE_LEN

from ..pylib.terms import TERMS, replacements
from ..pylib.util import FLAGS


class Base(TraitMatcher):
    """Base matcher object."""

    # Find tokens in the regex. Look for words that are not part of a group
    # name or a metacharacter. So, "word" not "<word>". Neither "(?P" nor "\b"
    word_re = regex.compile(r"""
        (?<! \(\?P< ) (?<! \(\? ) (?<! [\\] )
        \b (?P<word> [a-z]\w* ) \b """, FLAGS)

    trait_matchers = {}
    raw_groupers = {}
    raw_producers = []
    raw_regex_terms = []
    raw_shared_terms = []

    def __init__(self, name):
        super().__init__(name)

        self.title = name.replace('_', ' ').title()

        self.literal_terms = self.build_literal_terms()
        self.regex_terms = self.build_regex_terms()

        self.groupers = self.build_groupers()
        self.producers = self.build_producers()

        self.replace = replacements(self.name)

        # TODO: Delete this
        self.trait_matcher = Matcher(self.nlp.vocab)
        _ = [self.trait_matcher.add(k, v) for
             k, v in self.trait_matchers.items()]

    def build_regex_terms(self):
        """Get the regular expression terms relevant to this matcher."""
        if not self.raw_regex_terms:
            return []
        regex_terms = Matcher(self.nlp.vocab)
        for label in self.raw_regex_terms:
            regexp = TERMS['regexp'][label][0]['term']
            pattern = [{'TEXT': {'REGEX': regexp}}]
            regex_terms.add(label, [pattern], on_match=self.enrich)
        return regex_terms

    def build_literal_terms(self, attr='lower'):
        """Get terms specific for the matcher and shared terms."""
        attr = attr.upper()

        literal_terms = PhraseMatcher(self.nlp.vocab, attr='LOWER')

        shared = {k: v for k, v in TERMS['shared'].items()
                  if k in self.raw_shared_terms}

        combined = {**TERMS[self.name], **shared}
        for label, values in combined.items():
            patterns = [self.nlp.make_doc(t['term']) for t in values
                        if t['match_on'].upper() == attr]
            literal_terms.add(label, self.enrich, *patterns)
        return literal_terms

    def find_terms(self, text):
        """Find all terms in the text and return the resulting doc.

        There may be more than one matcher for the terms. Gather the results
        for each one and combine them. Then retokenize the doc to handle terms
        that span multiple tokens.
        """
        doc = self.nlp(text)

        matches = self.literal_terms(doc)

        if self.regex_terms:
            matches += self.regex_terms(doc)

        matches = self.leftmost_longest(matches)

        with doc.retokenize() as retokenizer:
            for match_id, start, end in matches:
                retokenizer.merge(doc[start:end])

        return doc

    def get_trait_matches(self, doc):
        """Get the trait matches."""
        # TODO: Delete this
        matches = self.trait_matcher(doc)
        if not matches:
            return []
        return self.leftmost_longest(matches)

    def build_groupers(self):
        """Create regular expressions out of the groupers."""
        groupers = {}
        for key, value in self.raw_groupers.items():
            if isinstance(value, list):
                value = '|'.join(f'(?:{v})' for v in value)
            groupers[key] = f'(?:{value})'
        return groupers

    def build_producers(self):
        """Create and compile regex out of the producers."""
        def _replace(match):
            word = match.group('word')
            return f'(?:{CODES[word]})'

        producers = []
        for p_func, p_regex in self.raw_producers:
            for g_name, g_regex in self.groupers.items():
                p_regex = p_regex.replace(g_name, g_regex)
            p_regex = self.word_re.sub(_replace, p_regex)
            p_regex = regex.compile(p_regex, FLAGS)
            producers.append([p_func, p_regex])
        return producers

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
