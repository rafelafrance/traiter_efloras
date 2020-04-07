"""Parse the trait."""


from .base import Base
from ..pylib.trait import Trait


class PlantDescriptor(Base):
    """Parse plant colors."""

    def parse(self, text):
        """parse the traits."""
        # trait = Trait(start=len(text), end=0)
        # raw_start, raw_end = len(text), 0
        sexual = []
        symmetry = []

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
