"""Parse the trait."""

from .matcher import Matcher
from ..pylib.convert_units import convert
from ..pylib.terms import CLOSE, CROSS, DASH, FLOAT, OPEN
from ..pylib.util import DotDict as Trait, to_positive_float


class PlantSize(Matcher):
    """Parse plant size notations."""

    trait_matchers = {
        'plant_part': [[{'_': {'term': 'plant_part'}}]],
        'size_min': [[OPEN, FLOAT, DASH, CLOSE]],
        'size_low': [[FLOAT]],
        'size_high': [[DASH, FLOAT]],
        'size_max': [[OPEN, DASH, FLOAT, CLOSE]],
        'cross': [[CROSS]],
        'length_units': [[{'_': {'term': 'length_units'}}]],
        'dimension': [[{'_': {'term': 'dimension'}}]],
        'part_location': [[{'_': {'term': 'part_location'}}]],
        'plant_sex': [[{'_': {'term': 'plant_sex'}}]],
        'up_to': [[{'LOWER': 'to'}, FLOAT]],
        'conjunction': [[{'POS': 'CCONJ'}]],
    }

    fsm = {
        'start': {
            'plant_part': {'state': 'length', 'set': 'part'},
            'part_location': {'state': 'plant_part', 'set': 'location'},
        },
        'plant_part': {
            'plant_part': {'state': 'length', 'set': 'part'},
            'size_min': {'state': 'start'},
            'size_low': {'state': 'start'},
            'size_high': {'state': 'start'},
            'size_max': {'state': 'start'},
            'cross': {'state': 'start'},
            'length_units': {'state': 'start'},
            'dimension': {'state': 'start'},
            'part_location': {'set': 'location'},
            'plant_sex': {'set': 'sex'},
            'up_to': {'state': 'start'},
            'conjunction': {'state': 'start'},
        },
        'length': {
            'plant_part': {'state': 'length', 'save': True, 'set': 'part'},
            'size_min': {
                'state': 'in_len', 'set': 'min_length', 'float': True},
            'size_low': {
                'state': 'in_len', 'set': 'low_length', 'float': True},
            'size_high': {
                'state': 'in_len', 'set': 'high_length', 'float': True},
            'size_max': {
                'state': 'in_len', 'set': 'max_length', 'float': True},
            'cross': {'state': 'width'},
            'length_units': {},
            'dimension': {},
            'part_location': {},
            'plant_sex': {'set': 'sex'},
            'up_to': {'state': 'in_len', 'set': 'high_length', 'float': True},
            'conjunction': {
                'state': 'length', 'save': True, 'carry': ('start', 'part')},
            'end': {'save': True},
        },
        'in_len': {
            'plant_part': {'state': 'length', 'save': True, 'set': 'part'},
            'size_min': {'set': 'min_length', 'float': True},
            'size_low': {'set': 'low_length', 'float': True},
            'size_high': {'set': 'high_length', 'float': True},
            'size_max': {'set': 'max_length', 'float': True},
            'cross': {'state': 'width'},
            'length_units': {'set': 'length_units'},
            'dimension': {'set': 'dimension', 'max_dist': 1},
            'part_location': {'set': 'location'},
            'plant_sex': {'set': 'sex'},
            'up_to': {'set': 'high_length', 'float': True},
            'conjunction': {
                'state': 'length', 'save': True, 'carry': ('start', 'part')},
            'end': {'save': True},
        },
        'width': {
            'plant_part': {'state': 'length', 'save': True, 'set': 'part'},
            'size_min': {'set': 'min_width', 'float': True},
            'size_low': {'set': 'low_width', 'float': True},
            'size_high': {'set': 'high_width', 'float': True},
            'size_max': {'set': 'max_width', 'float': True},
            'cross': {'state': 'start'},
            'length_units': {'set': 'width_units'},
            'dimension': {'set': 'dimension', 'max_dist': 1},
            'part_location': {'set': 'location'},
            'plant_sex': {'set': 'sex'},
            'up_to': {'set': 'high_width', 'float': True},
            'conjunction': {
                'state': 'length', 'save': True, 'carry': ('start', 'part')},
            'end': {'save': True},
        },
    }

    def parse(self, text):
        """parse the traits."""
        traits = []

        doc = self.find_terms(text)
        matches = self.get_trait_matches(doc)

        trait = Trait(start=-1)
        state = 'start'
        prev_end, max_dist = 0, len(doc)

        for match_id, start, end in matches:
            label = doc.vocab.strings[match_id]
            span = doc[start:end]
            norm = span.text.lower()

            action = self.fsm[state].get(label, {})

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
