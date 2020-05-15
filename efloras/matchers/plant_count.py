"""Parse the trait."""

from .base import Base, group2span
from ..pylib.util import DotDict as Trait, to_positive_int

FIELDS = ('min_count', 'low_count', 'high_count', 'max_count')


class PlantCount(Base):
    """Parse plant count notations."""

    def __init__(self, part):
        plant_part = f'{part}_part'
        name = f'{part}_count'

        super().__init__(name)

        self.use('sep')

        self.capture('min_count', """ open int (dash | dash_like) close """)
        self.capture('high_count', """ (dash | dash_like) int """)
        self.capture('max_count', """ open (dash | dash_like) int close """)

        self.capture('sex', 'plant_sex')

        self.grouper('reject', """
            length_units | cross | int | dash | dash_like | open | close
            | slash
            """)

        self.producer(self.convert, f"""
            sex? (?P<part> {plant_part} )
            (?P<value> min_count? (?P<low_count> int) high_count? max_count? )
            (?! reject ) """)

    @staticmethod
    def convert(doc, match, token_map):
        """Convert the matched term into a trait."""
        trait = Trait()

        span = group2span(doc, match, 'part', token_map)
        trait.start = span.start_char
        trait.part = span.text.lower()

        if span := group2span(doc, match, 'sex', token_map):
            trait.start = min(span.start_char, trait.start)
            trait.sex = span.text.lower()

        span = group2span(doc, match, 'value', token_map)
        trait.end = span.end_char

        for group in ('min_count', 'low_count', 'high_count', 'max_count'):
            if span := group2span(doc, match, group, token_map):
                trait[group] = to_positive_int(span.text)

        return trait


PLANT_COUNT = PlantCount('plant')
SEPAL_COUNT = PlantCount('sepal')
