"""Common color snippets."""

from traiter.new.rules.literals import Literals
from .base import Base


COLORS = Literals(literals=["""
    black blackish blue blueish brown brownish
    cream cream-yellow creamy crimson
    glaucous-pink gold golden golden-yellow gray gray-green green greenish
    grey grey-green
    ivory ivory-white
    lavendar lavender lemon lilac
    maroon
    olive olive-green orange orange-pink
    pink pink-purple pink-violet pinkish purple purpleish purplish
    red red-brown reddish rose rose-coloured
    salmon salmon-pink scarlet silver silvery stramineous straw-colored
    sulphur-yellow
    tan
    violet violetish
    white whitish
    yellow yellowish
    """.split()])

PREFIXES = Literals(literals=["""
    bright brighter
    dark darker deep deeper 
    light lighter
    often
    pale paler
    rarely
    slightly sometimes
    usually
    """.split() + ['usually', 'not']])

SUFFIXES = Literals(literals=["""
    lined lines longitudinal
    mottled
    spot spots spotted stripe striped stripes
    vein veined veins
    throated tinge tinged tinges tip tipped tips
    """.split()])

RENAME = {
    'blackish': 'black',
    'blueish': 'blue',
    'brownish': 'brown',
    'cream': 'white',
    'cream-yellow': 'yellow',
    'creamy': 'cream',
    'crimson': 'red',
    'glaucous-pink': 'pink',
    'golden-yellow': 'yellow',
    'greyish': 'gray',
    'greenish': 'green',
    'ivory': 'white',
    'lavendar': 'purple',
    'lavender': 'purple',
    'lemon': 'yellow',
    'lilac': 'purple',
    'maroon': 'red-brown',
    'olive-green': 'green',
    'pink-violet': 'pink-purple',
    'pinkish': 'pink',
    'purpleish': 'purple',
    'purplish': 'purple',
    'reddish': 'red',
    'rose': 'pink',
    'rose-coloured': 'pink',
    'salmon-pink': 'orange-pink',
    'scarlet': 'red',
    'silvery': 'silver',
    'stramineous': 'yellow',
    'straw-colored': 'yellow',
    'sulphur-yellow': 'yellow',
    'violet': 'purple',
    'violetish': 'purple',
    'whitish': 'white',
    'yellowish': 'yellow',
    }

PATTERNS = [
    [Literals(literals=[COLORS])],
    ]


def parser(plant_part):
    """Build a parser for the flower part."""
    return Base(f'{plant_part}_color', PATTERNS)


FLOWER_COLOR = parser('flower')
HYPANTHIUM_COLOR = parser('hypanthium')
SEPAL_COLOR = parser('sepal')
PETAL_COLOR = parser('petal')
CAYLX_COLOR = parser('calyx')
COROLLA_COLOR = parser('corolla')
