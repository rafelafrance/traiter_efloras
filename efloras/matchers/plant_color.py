"""Common color snippets."""

from spacy.matcher import PhraseMatcher, Matcher
from .base import Base
from ..pylib.trait import Trait


class PlantColor(Base):
    """Parse plant colors."""

    plant_part = [[{'_': {'term': 'PLANT_PART'}}]]
    color_phrase = [
        [
            {'_': {'term': 'COLOR_LEADER'}, 'OP': '?'},
            {'TEXT': '-', 'OP': '?'},
            {'_': {'term': 'COLOR'}},
            {'TEXT': '-', 'OP': '?'},
            {'_': {'term': 'COLOR_FOLLOWER'}, 'OP': '*'},
            ],
        [{'_': {'term': 'COLOR_LEADER'}}]
        ]

    def __init__(self):
        super().__init__('plant_color')
        self.term_matcher = PhraseMatcher(self.nlp.vocab, attr='LOWER')
        self.term_phrases()
        self.replace = self.term_replace()

        self.trait_matcher = Matcher(self.nlp.vocab)
        self.trait_matcher.add("PLANT_PART", self.plant_part)
        self.trait_matcher.add("COLOR_PHRASE", self.color_phrase)

    def parse(self, text):
        """parse the traits."""
        trait = Trait(
            part='', value='', raw_value='', start=len(text), end=0)
        raw_start, raw_end = len(text), 0

        doc = self.nlp(text)

        matches = self.term_matcher(doc)
        if not matches:
            return []
        matches = self.first_longest(matches)

        with doc.retokenize() as retokenizer:
            for match_id, start, end in matches:
                retokenizer.merge(doc[start:end])

        matches = self.trait_matcher(doc)
        if not matches:
            return []
        matches = self.first_longest(matches)

        colors = set()

        for match_id, start, end in matches:
            label = doc.vocab.strings[match_id]
            span = doc[start:end]
            norm = span.text.lower()
            trait.start = min(trait.start, span.start_char)
            trait.end = max(trait.end, span.end_char)

            if label == 'PLANT_PART':
                trait.part = norm
            else:
                raw_start = min(raw_start, span.start_char)
                raw_end = max(raw_end, span.end_char)
                words = [self.replace.get(t.text, t.text)
                         for t in span if t.text != '-']
                color = '-'.join(words)
                colors.add(color)

        trait.raw_value = text[raw_start:raw_end]
        trait.value = sorted(colors)
        return [trait]


PLANT_COLOR = PlantColor()
