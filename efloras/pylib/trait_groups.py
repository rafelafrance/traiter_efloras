"""The trait groups and what is being parsed for each."""

import regex
from .util import FLAGS
from ..parsers.plant_size import LEAF_SIZE, PETIOLE_SIZE
from ..parsers.plant_size import PETAL_SIZE, CALYX_SIZE
from ..parsers.plant_size import SEPAL_SIZE, FLOWER_SIZE
from ..parsers.plant_size import HYPANTHIUM_SIZE, COROLLA_SIZE
from ..parsers.plant_shape import LEAF_SHAPE, PETIOLE_SHAPE
from ..parsers.plant_shape import PETAL_SHAPE, CAYLX_SHAPE
from ..parsers.plant_shape import FLOWER_SHAPE, HYPANTHIUM_SHAPE
from ..parsers.plant_shape import COROLLA_SHAPE, SEPAL_SHAPE
from ..parsers.plant_color import FLOWER_COLOR, HYPANTHIUM_COLOR
from ..parsers.plant_color import SEPAL_COLOR, PETAL_COLOR
from ..parsers.plant_color import CAYLX_COLOR, COROLLA_COLOR
from ..parsers.plant_descriptors import SEXUAL_DESCRIPTOR, SYMMETRY_DESCRIPTOR
# from efloras.parsers.plant_count import SEPAL_COUNT


ALL = [SEXUAL_DESCRIPTOR, SYMMETRY_DESCRIPTOR]
CALYX = [CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR]
COROLLA = [COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR]
FLOWER = [FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR]
HYPANTHIUM = [HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR]
LEAF = [LEAF_SIZE, LEAF_SHAPE]
PETAL = [PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR]
PETIOLE = [PETIOLE_SIZE, PETIOLE_SHAPE]
SEPAL = [SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR]


TRAIT_GROUPS = {
    '2n': [],
    'anther heads': [],
    'basal leaves': (LEAF + PETIOLE),
    'basal rosettes': [],
    'capsules': [],
    'cauline leaves': (LEAF + PETIOLE),
    'caudices': [],
    'corollas': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'flowering stems': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'flowers': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'fruiting peduncles': [],
    'fruits': [],
    'herbs': [],
    'hypanthia': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'inflorescences': [],
    'inflorescenses': [],
    'leaf blades': (LEAF + PETIOLE),
    'leaflets': (LEAF + PETIOLE),
    'leaves': (LEAF + PETIOLE),
    'pedicels': [],
    'petioles': (LEAF + PETIOLE),
    'peduncles': [],
    'pepos': [],
    'petals': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'pistillate': [],
    'pistillate flowers': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'plants': [],
    'pollen': [],
    'racemes': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'seeds': [],
    'staminate corollas': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'staminate flowers': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'staminate inflorescences': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'staminate racemes': (
        FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'stolon leaves': [],
    'stolons': [],
    'stems': [],
    'tendrils': [],
    'vines': [],
    'x': [],
    }

# A quick & dirty way to get the ALL traits into every trait group
for value in TRAIT_GROUPS.values():
    value += ALL

TRAIT_GROUP_NAMES = sorted(
    TRAIT_GROUPS.keys(), key=lambda t: (len(t), t), reverse=True)

TRAIT_GROUPS_RE = ' | '.join(
    r' \s+ '.join(x.split()) for x in TRAIT_GROUP_NAMES)
TRAIT_GROUPS_RE = regex.compile(
    rf"""
        (?<! [\w:;,<>()] \s ) (?<! [\w:;,<>()] )
        \b ( {TRAIT_GROUPS_RE} ) \b
        """,
    flags=FLAGS)

TRAIT_NAMES = sorted({t.name for g in TRAIT_GROUPS.values() for t in g})


def expand_traits(args):
    """Expand traits using wildcards in given as arguments."""
    traits = set()
    for trait in args.trait:
        pattern = trait.replace('*', '.*').replace('?', '.?')
        pattern = regex.compile(pattern, regex.IGNORECASE)
        hits = {n for n in TRAIT_NAMES if pattern.search(n)}
        traits |= hits
    return sorted(traits)
