"""Common color snippets."""

from .base import Base, group2span
from ..pylib.util import DotDict as Trait


class PlantColor(Base):
    """Parse plant colors."""

    def convert(self, doc, match, token_map):
        """Convert the matched term into a trait."""
        trait = Trait()

        span = group2span(doc, match, 'part', token_map)
        trait.start = span.start_char
        trait.part = span.text.lower()

        span = group2span(doc, match, 'value', token_map)
        trait.end = span.end_char

        values = {}  # Sets do not preserve order
        value = []
        raw_start = span.end
        raw_end = span.start
        for token in span:
            term = token._.term

            if term in ('color_leader', 'color', 'color_follower'):
                raw_end = max(raw_end, token.i)
                raw_start = min(raw_start, token.i)

            if term in ('color_leader', 'color'):
                value.append(token.text.lower())
            elif term == 'color_follower':
                if value:
                    value.append(token.text.lower())
            elif term == 'dash':
                continue
            elif value:
                self.build_value(value, values)
                value = []
        if value:
            self.build_value(value, values)

        trait.value = list(values.keys())
        trait.raw_value = doc[raw_start:raw_end + 1].text

        return trait

    def build_value(self, value, values):
        """Add a color value."""
        value = '-'.join(self.replace.get(v, v) for v in value)
        value = self.replace.get(value, value)
        values[value] = 1

    term_list = """
        plant_part color color_leader color_follower dash """.split()

    raw_groupers = {
        'color_phrase': [
            """ color_leader* dash* color dash* color_follower* """,
        ],
    }

    raw_producers = [
        [convert, r"""
            (?P<part> plant_part ) (?P<value> color_phrase+ ) """],
    ]


PLANT_COLOR = PlantColor('plant_color')
