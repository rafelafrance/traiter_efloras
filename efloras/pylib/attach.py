"""Attach traits to a plant part.

We consider 3 levels of parts to a treatment sentence. For example:

    Male flowers: petals 4-6 red with 3 lobes.

1) "Male flowers": The primary part is the first part in a sentence. This may
    have a sex and/or a location etc. associated with it.
    If it does we need to transfer those transferable fields to any other part
    (or subpart) in the sentence.
        {'part': 'flowers', 'sex': 'male'}

2) "petals": This is considered a part of the flower (surprise!) and it gets
   the transferable fields. So the count trait "4-6" and the color trait "red"
   will get associated with the petals and it will receive the transferable
   fields like so:
        {'part': 'petal', 'sex': 'male'}
        {'petal_count': 'low': 4, 'high':6, 'sex': 'male'}
        {'petal_color': 'color': 'red', 'sex': 'male'}

3) "lobes": This is a subpart which is any "part" that can be associated with
    different parent parts. For instance, petals & leaves can have lobes. So
    it becomes:
        petal_lobe_count: {'low': 3, 'sex': 'male'}
    ** Also note that, in this case, the part comes after the trait.
"""

from traiter.util import Step  # pylint: disable=import-error

from efloras.matchers.descriptor import DESCRIPTOR_LABELS
from efloras.matchers.habit import HABIT_LABELS

# Labels that indicate plant-level parts
PLANT_LABELS = set(DESCRIPTOR_LABELS + HABIT_LABELS)

# The set of all values that get transferred to other parts
TRANSFER = set(""" sex location """.split())


def attach_traits_to_parts(sent):
    """Attach traits to a plant part."""
    augment = {}
    part = 'plant'
    subpart = ''

    tokens = [t for t in sent if t._.label == 'part']
    if tokens and tokens[0]._.label:
        data = tokens[0]._.data
        part = data['part']
        augment = {k: v for k, v in data.items() if k in TRANSFER}

    for token in sent:
        label = token._.label

        if label == 'subpart':
            subpart = f'_{subpart}'

        elif token._.step != Step.TRAIT or label == 'part':
            pass

        # Relabel the trait to match the plant part
        elif label not in PLANT_LABELS:
            dupe = part == label.split('_')[0]
            token._.label = label if dupe else f'{part}{subpart}_{label}'
        else:
            token._.label = f'plant_{label}'

        token._.data = {**augment, **token._.data}
