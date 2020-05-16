"""Common color snippets."""

import regex
from .base import Base, group2span
from ..pylib.util import DotDict as Trait


class PlantColor(Base):
    """Parse plant colors."""

    def __init__(self, part):
        plant_part = f'{part}_part'
        name = f'{part}_color'

        super().__init__(name)

        self.use('sep')

        self.capture('part', plant_part)

        self.capture('color_phrase', """
            (color_leader dash?)? (color | color_leader)
                dash* color_follower* """)

        self.grouper('noise', ' dash sep conj '.split())

        self.producer(self.convert, f"""
            part noise*
                ( noise* color_phrase (noise | color_follower)* )+ """)

        self.build()

        self.replace = self.get_term_replacements()

    def convert(self, doc, match, token_map):
        """Convert the matched term into a trait."""
        trait = Trait()

        span = group2span(doc, match, 'part', token_map)
        trait.start = span.start_char
        trait.part = span.text.lower()

        raw_start = len(doc)
        raw_end = 0

        values = {}
        for i, group in enumerate(match.captures('color_phrase')):
            span = group2span(doc, match, 'color_phrase', token_map, i)

            raw_start = min(span.start, raw_start)
            raw_end = max(span.end, raw_end)

            value = [v for v in regex.split(r'[\s-]+', span.text) if v]
            value = '-'.join(self.replace.get(v, v) for v in value)
            value = self.replace.get(value, value)
            values[value] = 1   # Sets do not preserve order but dicts do

        trait.value = list(values.keys())

        span = doc[raw_start:raw_end]
        trait.raw_value = span.text
        trait.end = span.end_char

        return trait


PLANT_COLOR = PlantColor('plant')
CAYLX_COLOR = PlantColor('calyx')
COROLLA_COLOR = PlantColor('corolla')
FLOWER_COLOR = PlantColor('flower')
HYPANTHIUM_COLOR = PlantColor('hypanthium')
PETAL_COLOR = PlantColor('petal')
SEPAL_COLOR = PlantColor('sepal')
