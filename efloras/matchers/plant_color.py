"""Common color snippets."""

from .base import Base
from ..pylib.trait import Trait


class PlantColor(Base):
    """Parse plant colors."""

    trait_matchers = {
        'PLANT_PART': [[{'_': {'term': 'PLANT_PART'}}]],
        'COLOR_PHRASE': [
            [
                {'_': {'term': 'COLOR_LEADER'}, 'OP': '?'},
                {'TEXT': '-', 'OP': '?'},
                {'_': {'term': 'COLOR'}},
                {'TEXT': '-', 'OP': '?'},
                {'_': {'term': 'COLOR_FOLLOWER'}, 'OP': '*'},
            ],
            [{'_': {'term': 'COLOR_LEADER'}}],
        ]}

    def parse(self, text):
        """parse the traits."""
        trait = Trait(start=len(text), end=0)
        raw_start, raw_end = len(text), 0

        doc = self.find_terms(text)
        matches = self.get_trait_matches(doc)

        colors = {}  # Sets do not preserve order

        for match_id, start, end in matches:
            label = doc.vocab.strings[match_id]
            span = doc[start:end]
            norm = span.text.lower()
            trait.end = max(trait.end, span.end_char)

            if label == 'PLANT_PART':
                trait.part = norm
                trait.start = span.start_char
            else:
                raw_start = min(raw_start, span.start_char)
                raw_end = max(raw_end, span.end_char)
                words = [self.replace.get(t.text, t.text)
                         for t in span if t.text != '-']
                color = '-'.join(words)
                colors[color] = 1

        trait.raw_value = text[raw_start:raw_end]
        trait.value = list(colors.keys())
        return [trait]


PLANT_COLOR = PlantColor('plant_color')
