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
from collections import namedtuple

from traiter.util import Step  # pylint: disable=import-error

from ..pylib.terms import LABELS
from ..matchers.all_matchers import ALL_PARTS, PART_LABELS, SUBPART_LABELS
from ..matchers.descriptor import DESCRIPTOR_LABELS

# Labels that indicate plant-level parts
PLANT_LEVEL_LABELS = set(DESCRIPTOR_LABELS)

# The set of all values that get transferred to other parts
TRANSFER = set(""" sex location """.split())

Suffix = namedtuple('Suffix', 'is_suffix leader')
SUFFIXES = {
    'with': '',
    'without': 'not ',
}
SUFFIX_END = {';', '.'}


def attach_traits_to_parts(sent):
    """Attach traits to a plant part."""
    subpart = ''
    suffix = Suffix(is_suffix=False, leader='')
    stack = []

    part = 'plant'
    augment_stack = [{}]
    parts = [t for t in sent if t._.label == 'part']
    if parts:
        data = parts[0]._.data
        part = data['part']
        augment_stack = [({k: v for k, v in data.items() if k in TRANSFER})]

    for token in sent:
        label = token._.label

        if token._.aux.get('attached'):
            continue

        elif token.lower_ in SUFFIXES:
            suffix = Suffix(is_suffix=True, leader=SUFFIXES.get(token.lower_))

        elif token.lower_ in SUFFIX_END:
            stack, suffix = adjust_stack(
                stack, part, subpart, augment_stack, suffix)

        elif token._.step != Step.TRAIT:
            continue

        elif suffix.is_suffix and label and label not in ALL_PARTS:
            stack.append(token)

        elif suffix.is_suffix and label in PART_LABELS:
            augment_stack = augment_data(augment_stack, token)
            part = token._.data['part']
            stack, suffix = adjust_stack(
                stack, part, subpart, augment_stack, suffix)

        elif suffix.is_suffix and label in SUBPART_LABELS:
            augment_stack = augment_data(augment_stack, token)
            subpart = token._.data['subpart']
            stack, suffix = adjust_stack(
                stack, part, subpart, augment_stack, suffix)

        elif label in PART_LABELS:
            augment_stack = augment_data(augment_stack, token)
            part = token._.data['part']

        elif label in SUBPART_LABELS:
            augment_stack = augment_data(augment_stack, token)
            subpart = token._.data['subpart']

        elif label in PLANT_LEVEL_LABELS:
            if not label.startswith('plant_'):
                token._.label = f'plant_{label}'

        else:
            update_token(token, label, part, subpart, augment_stack)


def augment_data(augment_stack, token):
    """Update the token's data field."""
    if augment := {k: v for k, v in token._.data.items() if k in TRANSFER}:
        if len(augment_stack) > 1:
            augment_stack[-1] = augment
        else:
            augment_stack.append(augment)
    token._.data = {**token._.data, **augment_stack[-1]}
    return augment_stack


def adjust_stack(stack, part, subpart, augment_stack, suffix):
    """Adjust all tokens on the suffix stack."""
    for token in stack:
        label = token._.label
        if suffix.leader:
            for key, value in token._.data.items():
                if key in LABELS and isinstance(value, str):
                    token._.data[key] = suffix.leader + token._.data[key]
        update_token(token, label, part, subpart, augment_stack)
    return [], Suffix(is_suffix=False, leader='')


def update_token(token, label, part, subpart, augment_stack):
    """Relabel the token and add the augment data."""
    label = f'{part}_{subpart}_{label}' if subpart else f'{part}_{label}'
    label = re.sub(r'_([^_]+)_\1', r'_\1', label)
    token._.label = re.sub(r'^([^_]+)_\1', r'\1', label)
    aug = augment_stack.pop() if len(augment_stack) > 1 else augment_stack[0]
    token._.data = {**token._.data, **aug}
