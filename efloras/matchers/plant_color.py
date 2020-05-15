"""Common color snippets."""

from .base import Base, group2span
from ..pylib.util import DotDict as Trait


class PlantColor(Base):
    """Parse plant colors."""

    def __init__(self, part):
        plant_part = f'{part}_part'
        name = f'{part}_color'

        super().__init__(name)

        self.grouper('color_phrase', """
            color_leader* dash* color dash* color_follower* """)

        self.producer(self.convert, f"""
            (?P<part> {plant_part} ) (?P<value> color_phrase+ ) """)

        self.build()

        self.replace = self.get_term_replacements()

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
            # print(term, value, token.text)

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


PLANT_COLOR = PlantColor('plant')
CAYLX_COLOR = PlantColor('calyx')
COROLLA_COLOR = PlantColor('corolla')
FLOWER_COLOR = PlantColor('flower')
HYPANTHIUM_COLOR = PlantColor('hypanthium')
PETAL_COLOR = PlantColor('petal')
SEPAL_COLOR = PlantColor('sepal')
