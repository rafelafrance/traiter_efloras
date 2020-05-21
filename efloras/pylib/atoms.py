"""List all of the matchers."""

import regex

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
    r'2\s*n': set(),
    'anther heads': set(),
    'anthers': set(),
    'asexual structures': set(),
    'bark': set(),
    'basal leaves': (LEAF | PETIOLE),
    'basal rosettes': set(),
    'branches': set(),
    'calyptra': set(),
    'capsule': FRUIT,
    'capsules': set(),
    'caudices': set(),
    'cauline leaves': (LEAF | PETIOLE),
    'corollas': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'flowering stems': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'flowers': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'fruiting catkins': set(),
    'fruiting peduncles': set(),
    'fruits': FRUIT,
    'herbs': set(),
    'hypanthia': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'inflorescences': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'inflorescenses': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'infructescences': set(),
    'leaf blade': (LEAF | PETIOLE),
    'leaf blades': (LEAF | PETIOLE),
    'leaflets': (LEAF | PETIOLE),
    'leaves': (LEAF | PETIOLE),
    'pedicels': set(),
    'peduncles': set(),
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
    'plants': set(),
    'pollen': set(),
    'protonematal flaps': set(),
    'racemes': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'samaras': set(),
    'seeds': SEED,
    'seta': set(),
    'seta superficial cells': set(),
    'sexual condition': set(),
    'shrubs': set(),
    'specialized asexual structures': set(),
    'spores': set(),
    'staminate corollas': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'staminate flowers': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'staminate inflorescences': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'staminate racemes': (
        FLOWER | HYPANTHIUM | SEPAL | PETAL | CALYX | COROLLA),
    'stem leaves': set(),
    'stems': set(),
    'stolon leaves': set(),
    'stolons': set(),
    'tendrils': set(),
    'thallose protonematal flaps': set(),
    'trees': set(),
    'twigs': set(),
    'vines': set(),
    'winter buds': set(),
    'wood': set(),
    'x': set(),
}

ATOMS = dict(sorted(ATOMS.items(), reverse=True, key=lambda a: len(a[0])))

ATOMIZER = ' | '.join(
    r' \s '.join(x.split()) for x in ATOMS.keys())
# ATOMIZER = regex.compile(
#     rf""" (?<! [\w:,<>()] \s) \b ( {ATOMIZER} ) \b  """, flags=FLAGS)

ATOMIZER = regex.compile(
    rf""" (?<= ^ | [.] \s* ) \b ( {ATOMIZER} ) \b  """, flags=FLAGS)
