"""Parse the trait."""

from .base import Base, group2span
from ..pylib.util import DotDict as Trait


class PlantDescriptor(Base):
    """Parse plant colors."""

    def __init__(self, part):
        self.descriptor = f'{part}_descriptor'

        super().__init__(self.descriptor)

        self.producer(self.convert, f""" (?P<value> {self.descriptor} ) """)

    @staticmethod
    def convert(doc, match, token_map):
        """Convert the matched term into a trait."""
        trait = Trait()

        span = group2span(doc, match, 'value', token_map)
        trait.start = span.start_char
        trait.end = span.end_char
        trait.value = span.text.lower()

        return trait


SEXUAL_DESCRIPTOR = PlantDescriptor('sexual')
SYMMETRY_DESCRIPTOR = PlantDescriptor('symmetry')
