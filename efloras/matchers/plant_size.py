"""Parse the trait."""

from .base import Base
from ..pylib.util import DotDict as Trait
from ..pylib.util import to_pos_float
from ..pylib.convert_units import convert


class PlantSize(Base):
    """Parse plant size notations."""

    trait_matchers = {
        'PLANT_PART': [[{'_': {'term': 'PLANT_PART'}}]],
        'SIZE_MIN': [
            [
                {'TEXT': {'REGEX': r'[(\[]'}},
                {'LIKE_NUM': True},
                {'TEXT': {'REGEX': r'[\–\-]'}},
                {'TEXT': {'REGEX': r'[)\]]'}},
            ]],
        'SIZE_LOW': [[{'LIKE_NUM': True}]],
        'SIZE_HIGH': [[
            {'TEXT': {'REGEX': r'[\–\-]'}},
            {'LIKE_NUM': True}
        ]],
        'SIZE_MAX': [
            [
                {'TEXT': {'REGEX': r'[(\[]'}},
                {'TEXT': {'REGEX': r'[\–\-]'}},
                {'LIKE_NUM': True},
                {'TEXT': {'REGEX': r'[)\]]'}},
            ]],
        'CROSS': [[{'TEXT': {'REGEX': r'[x×]'}}]],
        'LENGTH_UNITS': [[{'_': {'term': 'LENGTH_UNITS'}}]],
        'DIMENSION': [[{'_': {'term': 'DIMENSION'}}]],
    }

    def parse(self, text):
        """parse the traits."""
        traits = []

        doc = self.find_terms(text)
        matches = self.get_trait_matches(doc)

        # for token in doc:
        #     print(token.text, token._.term)

        trait = Trait(start=len(text), end=0)
        dim = 'length'

        for match_id, start, end in matches:
            label = doc.vocab.strings[match_id]
            span = doc[start:end]
            norm = span.text.lower()

            if label == 'PLANT_PART':
                dim = 'length'
                trait = Trait(
                    part=self.replace.get(norm, norm),
                    start=span.start_char)
            elif label == 'SIZE_MIN':
                trait['min_' + dim] = to_pos_float(norm)
            elif label == 'SIZE_LOW':
                trait['low_' + dim] = to_pos_float(norm)
            elif label == 'SIZE_HIGH':
                trait['high_' + dim] = to_pos_float(norm)
            elif label == 'SIZE_MAX':
                trait['max_' + dim] = to_pos_float(norm)
            elif label == 'CROSS':
                dim = 'width'
            elif label == 'LENGTH_UNITS':
                trait.units = norm
                trait.end = span.end_char
                for dim in ('length', 'width'):
                    for value in ('min', 'low', 'high', 'max'):
                        key = f'{value}_{dim}'
                        if key in trait:
                            value = trait[key]
                            trait[key] = convert(value, trait.units)
                traits.append(trait)
            elif label == 'DIMENSION':
                traits[-1].dimension = norm
                traits[-1].end = span.end_char

            # print(label, norm)

        return traits


PLANT_SIZE = PlantSize('plant_size')
