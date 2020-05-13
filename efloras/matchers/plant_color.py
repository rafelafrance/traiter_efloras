"""Common color snippets."""

from .base import Base
from ..pylib.terms import DASH_Q
from ..pylib.util import DotDict as Trait


def convert(self, doc, extended_match, starts, ends):
    """Convert the matched term into a trait."""
    _, start, end, match = extended_match

    trait = Trait(start=start, end=end)

    start = starts[match.start('part')]
    end = ends[match.end('part')]
    span = doc.char_span(start, end)
    trait.part = span.text.lower()

    start = starts[match.start('value')]
    end = ends[match.end('value')]
    span = doc.char_span(start, end)
    trait.raw_value = span.text

    values = {}  # Sets do not preserve order
    value = []
    for token in span:
        term = token._.term
        if term in ('color_leader', 'color', 'color_follower'):
            value.append(token.text.lower())
        elif term == 'dash':
            continue
        elif value:
            value = '-'.join(self.replace.get(v, v) for v in value)
            value = self.replace.get(value, value)
            values[value] = 1
            value = []
    if value:
        value = '-'.join(self.replace.get(v, v) for v in value)
        value = self.replace.get(value, value)
        values[value] = 1

    trait.value = list(values.keys())

    return trait


class PlantColor(Base):
    """Parse plant colors."""

    trait_matchers = {
        'plant_part': [[{'_': {'term': 'plant_part'}}]],
        'color_phrase': [
            [
                {'_': {'term': 'color_leader'}, 'OP': '?'},
                DASH_Q,
                {'_': {'term': 'color'}},
                DASH_Q,
                {'_': {'term': 'color_follower'}, 'OP': '*'},
            ],
            [{'_': {'term': 'color_leader'}}],
        ]}

    raw_regex_terms = """ dash """.split()

    raw_groupers = {
        'color_phrase': [
            """ (color_leader dash*)? color+ dash* color_follower* """,
            # """ color_leader """,
        ],
    }

    raw_producers = [
        [convert, r""" (?P<part> plant_part ) (?P<value> color_phrase+ ) """],
    ]

    def old_parse(self, text):
        """Keep this logic until it is replaced"""
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

            if label == 'plant_part':
                self.append_trait(
                    text, traits, trait, values, raw_start, raw_end)
                values = {}
                trait = Trait(
                    part=self.replace.get(norm, norm),
                    start=span.start_char,
                    end=span.end_char)
            elif label == 'color_phrase':
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
