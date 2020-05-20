"""List all of the matchers."""

import regex

from traiter.util import FLAGS


ALL = ['seasonal_descriptor', 'sexual_descriptor', 'symmetry_descriptor',
       'temporal_descriptor']
CALYX = ['calyx_size', 'caylx_shape', 'caylx_color']
COROLLA = ['corolla_size', 'corolla_shape', 'corolla_color']
FLOWER = ['flower_shape', 'flower_size', 'flower_color']
FRUIT = ['fruit_shape', 'fruit_size', 'fruit_color']
HYPANTHIUM = ['hypanthium_shape', 'hypanthium_size', 'hypanthium_color']
LEAF = ['leaf_size', 'leaf_shape']
PETAL = ['petal_size', 'petal_shape', 'petal_color']
PETIOLE = ['petiole_size', 'petiole_shape']
SEED = ['seed_size']
SEPAL = ['sepal_size', 'sepal_shape', 'sepal_color']


# Keywords used to split treatment into text atoms
ATOMS = {
    r'2n': [],
    'anther heads': [],
    'anthers': [],
    'asexual structures': [],
    'basal leaves': (LEAF + PETIOLE),
    'basal rosettes': [],
    'calyptra': [],
    'capsule': FRUIT,
    'capsules': [],
    'caudices': [],
    'cauline leaves': (LEAF + PETIOLE),
    'corollas': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'flowering stems': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'flowers': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'fruiting peduncles': [],
    'fruits': FRUIT,
    'herbs': [],
    'hypanthia': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'inflorescences': [],
    'inflorescenses': [],
    'leaf blades': (LEAF + PETIOLE),
    'leaflets': (LEAF + PETIOLE),
    'leaves': (LEAF + PETIOLE),
    'pedicels': [],
    'peduncles': [],
    'pepos': FRUIT,
    'petals': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'petioles': (LEAF + PETIOLE),
    'pistillate corollas': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'pistillate flowers': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'pistillate inflorescences': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'pistillate racemes': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'plants': [],
    'pollen': [],
    'protonematal flaps': [],
    'racemes': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'seeds': SEED,
    'seta': [],
    'seta superficial cells': [],
    'sexual condition': [],
    'specialized asexual structures': [],
    'spores': [],
    'staminate corollas': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'staminate flowers': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'staminate inflorescences': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'staminate racemes': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'stem leaves': [],
    'stems': [],
    'stolon leaves': [],
    'stolons': [],
    'tendrils': [],
    'thallose protonematal flaps': [],
    'vines': [],
    'x': [],
}

ATOMS = dict(sorted(ATOMS.items(), reverse=True, key=lambda x: len(x[0])))

ATOMIZER = ' | '.join(
    r' \s+ '.join(x.split()) for x in ATOMS.keys())
ATOMIZER = regex.compile(
    rf"""
        (?<! [\w:;,<>()] \s ) (?<! [\w:;,<>()] )
        \b ( {ATOMIZER} ) \b
        """,
    flags=FLAGS)
