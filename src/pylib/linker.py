"""Attach traits to a plant parts.

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

from ..matchers.matcher import PART_LABELS, SUBPART_LABELS
from ..matchers.descriptor import DESCRIPTOR_LABELS
from .terms import LABELS

# Labels that indicate plant-level parts
PLANT_LEVEL_LABELS = set(DESCRIPTOR_LABELS)

# The set of all values that get transferred to other parts
TRANSFER = set(""" sex location """.split())

# Handle infix notation
INFIX = {'with': '', 'without': 'not '}
INFIX_END = {';', '.'}
INFIX_SORT = {'part': 1, 'subpart': 0}


def linker(sent):
    """Attach traits to a plant part."""
    tokens = reorder_tokens(sent)
    fsm(tokens)


def reorder_tokens(sent):
    """Filter and reorder tokens to simplify the FSM."""
    tokens = []
    infix = []
    forward = True
    for token in sent:
        data = token._.data
        if token._.data.get('_skip'):
            continue
        if token.lower_ in INFIX:
            tokens.append(token)
            forward = False
        elif token.lower_ in INFIX_END:
            tokens += sort_infix(infix)
            forward = True
            infix = []
            tokens.append(token)
        elif data and forward:
            tokens.append(token)
        elif data:
            infix.append(token)
    tokens += sort_infix(infix)
    return tokens


def fsm(tokens):
    """Relabel the tokens and augment the data."""
    aug = {}
    part = 'plant'
    subpart = ''
    negate = ''

    for token in tokens:
        label = token.ent_type_
        data = token._.data

        if token._.data.get('_attached') or token._.data.get('_skip'):
            continue

        if label in PART_LABELS:
            part = data['part']
            token._.data = {**token._.data, **aug}
            subpart = ''
            aug = augment(aug, data)

        elif label in SUBPART_LABELS:
            subpart = data['subpart']
            aug = augment(aug, data)
            token._.data = {**token._.data, **aug}

        elif label in PLANT_LEVEL_LABELS:
            if not label.startswith('plant_'):
                token.ent_type_ = f'plant_{label}'

        elif token._.data.get('_subpart_attached'):
            token.ent_type_ = label_token(part, '', label)
            token._.data = {**token._.data, **aug}

        elif token.lower_ in INFIX:
            negate = INFIX[token.lower_]

        elif token.lower_ in INFIX_END:
            subpart = ''

        else:
            token.ent_type_ = label_token(part, subpart, label)
            if negate:
                for key, value in token._.data.items():
                    if key in LABELS and isinstance(value, str):
                        token._.data[key] = negate + token._.data[key]
            token._.data = {**token._.data, **aug}


def sort_infix(tokens):
    """Push the part and subpart tokens to the start of infix notation."""
    return sorted(tokens, key=lambda t: (INFIX_SORT.get(t.ent_type_, 9)))


def augment(aug, data):
    """Get augmented data."""
    aug2 = {k: v for k, v in data.items() if k in TRANSFER}
    return aug2 if aug2 else aug


def label_token(part, subpart, label):
    """Relabel the token and add the augment data."""
    label = f'{part}_{subpart}_{label}' if subpart else f'{part}_{label}'
    label = re.sub(r'_([^_]+)_\1', r'_\1', label)
    label = re.sub(r'^([^_]+)_\1', r'\1', label)
    return label
