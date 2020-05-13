"""Parse the trait."""

from functools import reduce

from .base import Base
from ..pylib.terms import CLOSE, DASH, DASH_LIKE, INT, OPEN, SEP
from ..pylib.util import DotDict as Trait, to_positive_int

FIELDS = ('min_count', 'low_count', 'high_count', 'max_count')


class PlantCount(Base):
    """Parse plant count notations."""

    trait_matchers = {
        'plant_part': [[{'_': {'term': 'plant_part'}}]],
        'count_min': [
            [OPEN, INT, DASH, CLOSE],
            [OPEN, INT, DASH_LIKE, CLOSE],
        ],
        'count_low': [[INT]],
        'count_high': [
            [DASH, INT],
            [DASH_LIKE, INT],
        ],
        'count_max': [
            [OPEN, DASH, INT, CLOSE],
            [OPEN, DASH_LIKE, INT, CLOSE],
        ],
        'length_units': [[{'_': {'term': 'length_units'}}]],
        'plant_sex': [[{'_': {'term': 'plant_sex'}}]],
        'sep': [[SEP]],
        # 'CONJUNCTION': [[{'POS': 'CCONJ'}]],
    }

    fsm = {
        'start': {
            'plant_part': {'state': 'count', 'set': 'part'},
            'plant_sex': {'set': 'sex', 'state': 'plant_part'},
        },
        'plant_part': {
            'plant_part': {'state': 'count', 'set': 'part'},
            'count_min': {'state': 'start'},
            'count_low': {'state': 'start'},
            'count_high': {'state': 'start'},
            'count_max': {'state': 'start'},
            'sep': {'state': 'start'},
            'plant_sex': {'state': 'plant_part', 'set': 'part'},
            'length_units': {'reject': True, 'max_dist': 1},
        },
        'count': {
            'plant_part': {'state': 'count', 'save': True, 'set': 'part'},
            'count_min': {'set': 'min_count', 'int': True},
            'count_low': {'set': 'low_count', 'int': True},
            'count_high': {'set': 'high_count', 'int': True},
            'count_max': {'set': 'max_count', 'int': True},
            'plant_sex': {'set': 'sex'},
            'length_units': {'reject': True, 'max_dist': 1},
            'sep': {'save': True, 'state': 'start'},
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
            if (action.get('reject')
                    and dist <= action.get('max_dist', max_dist)):
                trait = Trait(start=-1)
                continue

            if field := action.get('set'):
                if action.get('int'):
                    trait[field] = to_positive_int(norm)
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

        if reduce(lambda x, y: x | (trait.get(y) is not None),
                  FIELDS, False):
            traits.append(trait)


PLANT_COUNT = PlantCount('plant_count')
