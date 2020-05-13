"""Base matcher object."""

import regex
from spacy.matcher import Matcher, PhraseMatcher
from traiter.matcher import Matcher as TraitMatcher

from ..pylib.terms import TERMS, replacements
from ..pylib.util import FLAGS


class Base(TraitMatcher):
    """Base matcher object."""

    # Find tokens in the regex. Look for words that are not part of a group
    # name or a metacharacter. So, "word" not "<word>". Neither "(?P" nor "\b"
    word_re = regex.compile(r"""
        (?<! \(\?P< ) (?<! \(\? ) (?<! [\\] ) \b ( [a-z]\w* ) \b """, FLAGS)

    split_re = regex.compile(r""" (?<= [\w?+*)] ) \s+ (?= [\w(] ) """, FLAGS)

    trait_matchers = {}
    raw_groupers = {}
    raw_producers = []
    raw_regex_terms = []

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
            regex_terms.add(label, [pattern], on_match=self.term_label)
        return regex_terms

    def build_literal_terms(self, attr='lower'):
        """Get terms specific for the matcher and shared terms."""
        attr = attr.upper()

        literal_terms = PhraseMatcher(self.nlp.vocab, attr='LOWER')

        combined = {**TERMS[self.name], **TERMS['shared']}
        for label, values in combined.items():
            patterns = [self.nlp.make_doc(t['term']) for t in values
                        if t['match_on'].upper() == attr]
            literal_terms.add(label, self.term_label, *patterns)
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

        # for token in doc:
        #     print(f'[{token._.term}] {token.text}')

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
        producers = []
        for p_func, p_regex in self.raw_producers:
            for g_name, g_regex in self.groupers.items():
                p_regex = p_regex.replace(g_name, g_regex)
            p_regex = self.word_re.sub(r'(?:\1)', p_regex)
            p_regex = r'\s?'.join(self.split_re.split(p_regex))
            p_regex = ''.join(p_regex.split())
            p_regex = regex.compile(p_regex, FLAGS)
            producers.append([p_func, p_regex])
        return producers

    def parse(self, text):
        """parse the traits."""
        doc = self.find_terms(text)

        starts = {}
        ends = {}
        terms = []

        term_start = 0
        for token in doc:
            term = token._.term
            if not term:
                continue
            terms.append(term)
            starts[term_start] = token.idx
            end = term_start + len(term)
            ends[end] = token.idx + len(token)
            term_start = end + 1
        string = ' '.join(terms)

        matches = []
        print(text)
        print(string)
        for func, regexp in self.producers:
            print(regexp)
            for match in regexp.finditer(string):
                start, end = match.span()
                print(match)
                matches.append((func, starts[start], ends[end], match))

        matches = self.leftmost_longest(matches)

        all_traits = []
        for extended_match in matches:
            action, *_ = extended_match

            traits = action(self, doc, extended_match, starts, ends)

            if not traits:
                continue

            all_traits += traits if isinstance(traits, list) else [traits]

            return all_traits
