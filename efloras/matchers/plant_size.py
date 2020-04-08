"""Parse the trait."""

from .base import Base
from ..pylib.util import DotDict as Trait
from ..pylib.util import to_positive_float
from ..pylib.convert_units import convert
from ..pylib.terms import CLOSE, CROSS, DASH, FLOAT, OPEN


class PlantSize(Base):
    """Parse plant size notations."""

    trait_matchers = {
        'PLANT_PART': [[{'_': {'term': 'PLANT_PART'}}]],
        'SIZE_MIN': [[OPEN, FLOAT, DASH, CLOSE]],
        'SIZE_LOW': [[FLOAT]],
        'SIZE_HIGH': [[DASH, FLOAT]],
        'SIZE_MAX': [[OPEN, DASH, FLOAT, CLOSE]],
        'CROSS': [[CROSS]],
        'LENGTH_UNITS': [[{'_': {'term': 'LENGTH_UNITS'}}]],
        'DIMENSION': [[{'_': {'term': 'DIMENSION'}}]],
        'PART_LOCATION': [[{'_': {'term': 'PART_LOCATION'}}]],
        'PLANT_SEX': [[{'_': {'term': 'PLANT_SEX'}}]],
        'UP_TO': [[{'LOWER': 'to'}, FLOAT]],
        'CONJUNCTION': [[{'POS': 'CCONJ'}]],
    }

    fsm = {
        'start': {
            'PLANT_PART': {'state': 'length', 'set': 'part'},
            'PART_LOCATION': {'state': 'plant_part', 'set': 'location'},
        },
        'plant_part': {
            'PLANT_PART': {'state': 'length', 'set': 'part'},
            'SIZE_MIN': {'state': 'start'},
            'SIZE_LOW': {'state': 'start'},
            'SIZE_HIGH': {'state': 'start'},
            'SIZE_MAX': {'state': 'start'},
            'CROSS': {'state': 'start'},
            'LENGTH_UNITS': {'state': 'start'},
            'DIMENSION': {'state': 'start'},
            'PART_LOCATION': {'set': 'location'},
            'PLANT_SEX': {'set': 'sex'},
            'UP_TO': {'state': 'start'},
            'CONJUNCTION': {'state': 'start'},
        },
        'length': {
            'PLANT_PART': {'state': 'length', 'save': True, 'set': 'part'},
            'SIZE_MIN': {
                'state': 'in_len', 'set': 'min_length', 'float': True},
            'SIZE_LOW': {
                'state': 'in_len', 'set': 'low_length', 'float': True},
            'SIZE_HIGH': {
                'state': 'in_len', 'set': 'high_length', 'float': True},
            'SIZE_MAX': {
                'state': 'in_len', 'set': 'max_length', 'float': True},
            'CROSS': {'state': 'width'},
            'LENGTH_UNITS': {},
            'DIMENSION': {},
            'PART_LOCATION': {},
            'PLANT_SEX': {'set': 'sex'},
            'UP_TO': {'state': 'in_len', 'set': 'high_length', 'float': True},
            'CONJUNCTION': {
                'state': 'length', 'save': True, 'carry': ('start', 'part')},
            'end': {'save': True},
        },
        'in_len': {
            'PLANT_PART': {'state': 'length', 'save': True, 'set': 'part'},
            'SIZE_MIN': {'set': 'min_length', 'float': True},
            'SIZE_LOW': {'set': 'low_length', 'float': True},
            'SIZE_HIGH': {'set': 'high_length', 'float': True},
            'SIZE_MAX': {'set': 'max_length', 'float': True},
            'CROSS': {'state': 'width'},
            'LENGTH_UNITS': {'set': 'length_units'},
            'DIMENSION': {'set': 'dimension', 'max_dist': 1},
            'PART_LOCATION': {'set': 'location'},
            'PLANT_SEX': {'set': 'sex'},
            'UP_TO': {'set': 'high_length', 'float': True},
            'CONJUNCTION': {
                'state': 'length', 'save': True, 'carry': ('start', 'part')},
            'end': {'save': True},
        },
        'width': {
            'PLANT_PART': {'state': 'length', 'save': True, 'set': 'part'},
            'SIZE_MIN': {'set': 'min_width', 'float': True},
            'SIZE_LOW': {'set': 'low_width', 'float': True},
            'SIZE_HIGH': {'set': 'high_width', 'float': True},
            'SIZE_MAX': {'set': 'max_width', 'float': True},
            'CROSS': {'state': 'start'},
            'LENGTH_UNITS': {'set': 'width_units'},
            'DIMENSION': {'set': 'dimension', 'max_dist': 1},
            'PART_LOCATION': {'set': 'location'},
            'PLANT_SEX': {'set': 'sex'},
            'UP_TO': {'set': 'high_width', 'float': True},
            'CONJUNCTION': {
                'state': 'length', 'save': True, 'carry': ('start', 'part')},
            'end': {'save': True},
        },
    }

    def parse(self, text):
        """parse the traits."""
        traits = []

        doc = self.find_terms(text)
        matches = self.get_trait_matches(doc)

        # print('\n'.join([f'{t.text} {t.pos_} {t._.term}' for t in doc]))

        trait = Trait(start=-1)
        state = 'start'
        prev_end, max_dist = 0, len(doc)

        for match_id, start, end in matches:
            label = doc.vocab.strings[match_id]
            span = doc[start:end]
            norm = span.text.lower()

            action = self.fsm[state].get(label, {})

            # print(f'{label} {norm}')

            if action.get('save'):
                self.append_trait(traits, trait)
                old = trait
                trait = Trait(start=-1)
                if carry := action.get('carry'):
                    for field in carry:
                        trait[field] = old[field]

            dist = start - prev_end
            if dist > action.get('max_dist', max_dist):
                continue

            if field := action.get('set'):
                if action.get('float'):
                    trait[field] = to_positive_float(norm)
                else:
                    trait[field] = self.replace.get(norm, norm)

            if trait.start < 0:
                trait.start = span.start_char
            trait.end = span.end_char

            state = action.get('state', state)
            prev_end = end

        action = self.fsm[state].get('end', {})
        if action.get('save'):
            self.append_trait(traits, trait)

        return traits

    @staticmethod
    def append_trait(traits, trait):
        """Check if a trait is valid, update & save it if it is."""
        # It must have a plant part
        if not trait.get('part'):
            return

        # It must have units. Make sure we have units for all values
        if trait.get('width_units'):
            if trait.get('length_units'):
                trait.units = [trait.length_units, trait.width_units]
            else:
                trait.length_units = trait.width_units
                trait.units = trait.width_units
        elif trait.get('length_units'):
            trait.units = trait.length_units
            trait.width_units = trait.length_units
        else:
            return

        has_value = False
        for dim in ('length', 'width'):
            units = trait[f'{dim}_units']
            for name in ('min', 'low', 'high', 'max'):
                field = f'{name}_{dim}'
                if field in trait:
                    has_value = True
                    value = trait[field]
                    trait[field] = convert(value, units)

        if has_value:
            del trait['length_units']
            del trait['width_units']
            traits.append(trait)


PLANT_SIZE = PlantSize('plant_size')
