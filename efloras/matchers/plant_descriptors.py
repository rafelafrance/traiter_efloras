"""Parse the trait."""

from .base import Base
from ..pylib.util import DotDict as Trait


class PlantDescriptor(Base):
    """Parse plant colors."""

    def parse(self, text):
        """parse the traits."""
        sexual, symmetry = [], []

        doc = self.find_terms(text)

        for token in doc:
            label = token._.term

            if label == 'SEXUAL_DESCRIPTOR':
                sexual.append(Trait(
                    value=token.text.lower(),
                    start=token.idx,
                    end=token.idx + len(token)
                ))
            elif label == 'SYMMETRY_DESCRIPTOR':
                symmetry.append(Trait(
                    value=token.text.lower(),
                    start=token.idx,
                    end=token.idx + len(token)
                ))

        return sexual + symmetry


PLANT_DESCRIPTOR = PlantDescriptor('plant_descriptor')
