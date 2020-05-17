"""Parse the trait."""

import regex

from .base import Base, group2span, TERMS
from ..pylib.util import DotDict as Trait


class PlantShape(Base):
    """Parse plant colors."""

    def __init__(self, part):
        plant_part = f'{part}_part'
        name = f'{part}_shape'

        super().__init__(name)

        self.capture('part', plant_part)

        self.capture('shape_phrase', """
            ( shape_starter joiner? )* ( shape | shape_starter) dash* shape*
            """)

        self.grouper('joiner', r""" dash conj prep """.split())
        self.grouper('noise', """ dash sep conj prep """.split())

        self.producer(self.convert, """
            part noise* ( noise* shape_phrase )+
            """)

        self.build()

        self.replace = self.get_term_replacements()
        self.shapes = TERMS['shape']

    def convert(self, doc, match, token_map):
        """Convert the matched term into a trait."""
        trait = Trait()

        span = group2span(doc, match, 'part', token_map)
        trait.start = span.start_char
        trait.part = span.text.lower()

        raw_start = len(doc)
        raw_end = 0

        values = {}
        for i, group in enumerate(match.captures('shape_phrase')):
            span = group2span(doc, match, 'shape_phrase', token_map, i)

            raw_start = min(span.start, raw_start)
            raw_end = max(span.end, raw_end)

            value = [v for v in regex.split(r'(?<!\d)-+|\s+', span.text)
                     if v and v in self.shapes]
            value = '-'.join(self.replace.get(v, v) for v in value)
            value = self.replace.get(value, value)
            if value:
                values[value] = 1   # Sets do not preserve order but dicts do

        trait.value = list(values.keys())

        span = doc[raw_start:raw_end]
        trait.raw_value = span.text
        trait.end = span.end_char

        return trait


PLANT_SHAPE = PlantShape('plant')
CAYLX_SHAPE = PlantShape('calyx')
COROLLA_SHAPE = PlantShape('corolla')
FLOWER_SHAPE = PlantShape('flower')
HYPANTHIUM_SHAPE = PlantShape('hypanthium')
LEAF_SHAPE = PlantShape('leaf')
PETAL_SHAPE = PlantShape('petal')
PETIOLE_SHAPE = PlantShape('petiole')
SEPAL_SHAPE = PlantShape('sepal')
