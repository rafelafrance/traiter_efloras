"""The rulers and how they map to ."""

import regex
from efloras.pylib.util import FLAGS
from efloras.rulers.plant_color import FLOWER_COLOR, HYPANTHIUM_COLOR


ALL_RULERS = {
    '2n': [],
    'anther heads': [],
    'basal leaves': [
        # LEAF_SIZE, LEAF_SHAPE,
        # PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'basal rosettes': [],
    'capsules': [],
    'cauline leaves': [
        # LEAF_SIZE, LEAF_SHAPE,
        # PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'caudices': [],
    'corollas': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'flowering stems': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'flowers': [
        FLOWER_COLOR,
        HYPANTHIUM_COLOR,
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'fruiting peduncles': [],
    'fruits': [],
    'herbs': [],
    'hypanthia': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'inflorescences': [
        ],
    'inflorescenses': [
        ],
    'leaf blades': [
        # LEAF_SIZE, LEAF_SHAPE,
        # PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'leaflets': [
        # LEAF_SIZE, LEAF_SHAPE,
        # PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'leaves': [
        # LEAF_SIZE, LEAF_SHAPE,
        # PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'pedicels': [],
    'petioles': [
        # LEAF_SIZE, LEAF_SHAPE,
        # PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'peduncles': [],
    'pepos': [],
    'petals': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'pistillate': [],
    'pistillate flowers': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'plants': [],
    'pollen': [],
    'racemes': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'seeds': [],
    'staminate corollas': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'staminate flowers': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'staminate inflorescences': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'staminate racemes': [
        # FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        # HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        # SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        # PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        # CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        # COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'stolon leaves': [],
    'stolons': [],
    'stems': [],
    'tendrils': [],
    'vines': [],
    'x': [],
    }

RULER_NAMES = sorted(
    ALL_RULERS.keys(), key=lambda t: (len(t), t), reverse=True)

RULER_GROUPS_RE = ' | '.join(
    r' \s+ '.join(x.split()) for x in RULER_NAMES)
RULER_GROUPS_RE = regex.compile(
    rf"""
        (?<! [\w:;,<>()] \s ) (?<! [\w:;,<>()] )
        \b ( {RULER_GROUPS_RE} ) \b
        """,
    flags=FLAGS)

TRAIT_NAMES = sorted({t.name for g in ALL_RULERS.values() for t in g})


def expand_traits(args):
    """Expand traits using wildcards in given as arguments."""
    traits = set()
    for trait in args.trait:
        pattern = trait.replace('*', '.*').replace('?', '.?')
        pattern = regex.compile(pattern, regex.IGNORECASE)
        hits = {n for n in TRAIT_NAMES if pattern.search(n)}
        traits |= hits
    return sorted(traits)
