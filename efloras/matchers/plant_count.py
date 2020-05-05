"""Parse the trait."""

from functools import reduce
from .base import Base
from ..pylib.util import DotDict as Trait
from ..pylib.util import to_positive_int
from ..pylib.terms import CLOSE, DASH, DASH_LIKE, INT, OPEN, STOP_PUNCT


FIELDS = ('min_count', 'low_count', 'high_count', 'max_count')


class PlantCount(Base):
    """Parse plant count notations."""

    trait_matchers = {
        'PLANT_PART': [[{'_': {'term': 'PLANT_PART'}}]],
        'COUNT_MIN': [
            [OPEN, INT, DASH, CLOSE],
            [OPEN, INT, DASH_LIKE, CLOSE],
        ],
        'COUNT_LOW': [[INT]],
        'COUNT_HIGH': [
            [DASH, INT],
            [DASH_LIKE, INT],
        ],
        'COUNT_MAX': [
            [OPEN, DASH, INT, CLOSE],
            [OPEN, DASH_LIKE, INT, CLOSE],
        ],
        'LENGTH_UNITS': [[{'_': {'term': 'LENGTH_UNITS'}}]],
        'PLANT_SEX': [[{'_': {'term': 'PLANT_SEX'}}]],
        'STOP_PUNCT': [[STOP_PUNCT]],
        # 'CONJUNCTION': [[{'POS': 'CCONJ'}]],
    }

    fsm = {
        'start': {
            'PLANT_PART': {'state': 'count', 'set': 'part'},
            'PLANT_SEX': {'set': 'sex', 'state': 'plant_part'},
        },
        'plant_part': {
            'PLANT_PART': {'state': 'count', 'set': 'part'},
            'COUNT_MIN': {'state': 'start'},
            'COUNT_LOW': {'state': 'start'},
            'COUNT_HIGH': {'state': 'start'},
            'COUNT_MAX': {'state': 'start'},
            'STOP_PUNCT': {'state': 'start'},
            'PLANT_SEX': {'state': 'plant_part', 'set': 'part'},
            'LENGTH_UNITS': {'reject': True, 'max_dist': 1},
        },
        'count': {
            'PLANT_PART': {'state': 'count', 'save': True, 'set': 'part'},
            'COUNT_MIN': {'set': 'min_count', 'int': True},
            'COUNT_LOW': {'set': 'low_count', 'int': True},
            'COUNT_HIGH': {'set': 'high_count', 'int': True},
            'COUNT_MAX': {'set': 'max_count', 'int': True},
            'LENGTH_UNITS': {'reject': True, 'max_dist': 1},
            'PLANT_SEX': {'set': 'sex'},
            'STOP_PUNCT': {'save': True, 'state': 'start'},
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
