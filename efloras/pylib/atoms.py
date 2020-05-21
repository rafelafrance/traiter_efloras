"""List all of the matchers."""

import regex

from traiter.spacy_nlp import NLP
from traiter.util import FLAGS  # pylint: disable=import-error


DESCRIPTOR = set(""" seasonal_descriptor sexual_descriptor symmetry_descriptor
    temporal_descriptor """.split())
CALYX = {'calyx_size', 'caylx_shape', 'caylx_color'}
COROLLA = {'corolla_size', 'corolla_shape', 'corolla_color'}
FLOWER = {'flower_shape', 'flower_size', 'flower_color'}
FRUIT = {'fruit_shape', 'fruit_size', 'fruit_color'}
HYPANTHIUM = {'hypanthium_shape', 'hypanthium_size', 'hypanthium_color'}
LEAF = {'leaf_size', 'leaf_shape'}
PETAL = {'petal_size', 'petal_shape', 'petal_color'}
PETIOLE = {'petiole_size', 'petiole_shape'}
SEED = {'seed_size'}
SEPAL = {'sepal_size', 'sepal_shape', 'sepal_color'}


# Keywords used to split treatment into text atoms
ATOMS = {
    'basal leaves': (LEAF | PETIOLE),
    'capsule': FRUIT,
    'cauline leaves': (LEAF | PETIOLE),
    'corollas': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'flowering': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'flowering stems': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'flowers': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'fruits': FRUIT,
    'hypanthia': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'inflorescences': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'inflorescenses': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'leaf blade': (LEAF | PETIOLE),
    'leaf blades': (LEAF | PETIOLE),
    'leaflets': (LEAF | PETIOLE),
    'leaves': (LEAF | PETIOLE),
    'pepos': FRUIT,
    'petals': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'petioles': (LEAF | PETIOLE),
    'pistillate corollas': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'pistillate flowers': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'pistillate inflorescences': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'pistillate racemes': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'racemes': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'seeds': SEED,
    'staminate corollas': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'staminate flowers': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'staminate inflorescences': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'staminate racemes': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'stem leaves': (LEAF | PETIOLE),
}

ATOMS = dict(sorted(ATOMS.items(), reverse=True, key=lambda a: len(a[0])))

ATOMIZER = ' | '.join(
    r' \s '.join(x.split()) for x in ATOMS.keys())
# ATOMIZER = regex.compile(
#     rf""" (?<! [\w:,<>()] \s) \b ( {ATOMIZER} ) \b  """, flags=FLAGS)
ATOMIZER = regex.compile(
    rf""" (?<= ^ \s* | [.] \s* ) \b ( {ATOMIZER} ) \b  """, flags=FLAGS)


def atomize(text):
    """Break the text into atoms."""
    doc = NLP(text)

    atoms = []

    for sent in doc.sents:
        atom = {
            'start': sent.start_char,
            'end': sent.end_char,
            'last': sent.end,
        }

        if (name := sent[:1].text.lower()) in ATOMS:
            atom['name'] = name
            atoms.append(atom)

        elif (name := sent[:2].text.lower()) in ATOMS:
            atom['name'] = name
            atoms.append(atom)

        # elif atoms and text[atoms[-1]['end']] != '.':
        #     atoms[-1]['end'] = sent.end_char
        #     atoms[-1]['last'] = sent.end

    return atoms
