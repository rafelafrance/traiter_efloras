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

import re

from traiter.util import Step  # pylint: disable=import-error

from .terms import REPLACE
from ..matchers.all_matchers import ALL_PARTS, PART_LABELS, SUBPART_LABELS
from ..matchers.descriptor import DESCRIPTOR_LABELS

# Labels that indicate plant-level parts
PLANT_LEVEL_LABELS = set(DESCRIPTOR_LABELS)

# The set of all values that get transferred to other parts
TRANSFER = set(""" sex location """.split())

SUFFIX_START = {'with'}
SUFFIX_END = {';', '.'}


# TODO: Replace as much of this function as practical with "attach" patterns
def attach_traits_to_parts(sent):
    """Attach traits to a plant part."""
    augment = {}
    part = 'plant'
    subpart = ''
    suffix = False  # Does the trait follow the part or lead it
    stack = []

    parts = [t for t in sent if t._.label == 'part']
    if parts:
        data = parts[0]._.data
        part = data['part']
        augment = {k: v for k, v in data.items() if k in TRANSFER}

    for token in sent:
        label = token._.label

        if token._.aux.get('attached'):
            continue

        elif token.lower_ in SUFFIX_START:
            suffix = True

        elif token.lower_ in SUFFIX_END:
            stack, suffix = adjust_stack(stack, part, subpart, augment)

        elif token._.step != Step.TRAIT:
            continue

        elif suffix and label and label not in ALL_PARTS:
            stack.append(token)

        elif suffix and label in PART_LABELS:
            token._.data = {**token._.data, **augment}
            part = token._.data['part']
            stack, suffix = adjust_stack(stack, part, subpart, augment)

        elif suffix and label in SUBPART_LABELS:
            token._.data = {**token._.data, **augment}
            subpart = token._.data['subpart']
            subpart = REPLACE.get(subpart, subpart)
            stack, suffix = adjust_stack(stack, part, subpart, augment)

        elif label in PART_LABELS:
            part = token._.data['part']
            token._.data = {**token._.data, **augment}

        elif label in SUBPART_LABELS:
            subpart = token._.data['subpart']
            subpart = REPLACE.get(subpart, subpart)
            token._.data = {**token._.data, **augment}

        elif label in PLANT_LEVEL_LABELS:
            if not label.startswith('plant_'):
                token._.label = f'plant_{label}'

        else:
            update_token(token, label, part, subpart, augment)


def adjust_stack(stack, part, subpart, augment):
    """Adjust all tokens on the suffix stack."""
    for saved_token in stack:
        label = saved_token._.label
        update_token(saved_token, label, part, subpart, augment)
    return [], False


def update_token(token, label, part, subpart, augment):
    """Relabel the token and add the augment data."""
    label = f'{part}_{subpart}_{label}' if subpart else f'{part}_{label}'
    label = re.sub(r'_([^_]+)_\1', r'_\1', label)
    token._.label = re.sub(r'^([^_]+)_\1', r'\1', label)
    token._.data = {**token._.data, **augment}
