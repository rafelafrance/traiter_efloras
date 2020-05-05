"""Common color snippets."""

from .base import Base
from ..pylib.terms import DASH_Q
from ..pylib.util import DotDict as Trait


class PlantColor(Base):
    """Parse plant colors."""

    trait_matchers = {
        'PLANT_PART': [[{'_': {'term': 'PLANT_PART'}}]],
        'COLOR_PHRASE': [
            [
                {'_': {'term': 'COLOR_LEADER'}, 'OP': '?'},
                DASH_Q,
                {'_': {'term': 'COLOR'}},
                DASH_Q,
                {'_': {'term': 'COLOR_FOLLOWER'}, 'OP': '*'},
            ],
            [{'_': {'term': 'COLOR_LEADER'}}],
        ]}

    def parse(self, text):
        """parse the traits."""
        traits = []

        doc = self.find_terms(text)
        matches = self.get_trait_matches(doc)

        values = {}  # Sets do not preserve order
        trait = Trait(start=len(text), end=0)
        raw_start, raw_end = len(text), 0

        for match_id, start, end in matches:
            label = doc.vocab.strings[match_id]
            span = doc[start:end]
            norm = span.text.lower()
            trait.end = max(trait.end, span.end_char)

            if label == 'PLANT_PART':
                self.append_trait(
                    text, traits, trait, values, raw_start, raw_end)
                values = {}
                trait = Trait(
                    part=self.replace.get(norm, norm),
                    start=span.start_char,
                    end=span.end_char)
            elif label == 'COLOR_PHRASE':
                raw_start = min(raw_start, span.start_char)
                raw_end = max(raw_end, span.end_char)
                words = [self.replace.get(t.text, t.text)
                         for t in span if t.text != '-']
                color = '-'.join(words)
                values[color] = 1

        self.append_trait(text, traits, trait, values, raw_start, raw_end)
        return traits

    def append_trait(self, text, traits, trait, values, raw_start, raw_end):
        """Append trait to the end of the traits list."""
        values = [self.replace.get(c, c) for c in values if c]
        if values:
            trait.raw_value = text[raw_start:raw_end]
            trait.value = values
            traits.append(trait)


PLANT_COLOR = PlantColor('plant_color')
