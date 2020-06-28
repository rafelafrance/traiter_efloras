"""A list of all matchers."""
from .attach import ATTACH
from .color import COLOR
from .count import COUNT
from .descriptor import DESCRIPTOR
from .margin import MARGIN_SHAPE
from .part import PART
from .part_location import PART_LOCATION
from .phrase import PHRASE
from .range import RANGE
from .shape import SHAPE
from .size import SIZE
from .subpart import SUBPART
from .suffix_count import SUFFIX_COUNT
from ..pylib.util import TRAIT_STEP

PARTS = [PART, SUBPART]
TRAITS = [
    ATTACH, COLOR, COUNT, DESCRIPTOR, MARGIN_SHAPE, PART_LOCATION, PHRASE,
    RANGE, SHAPE, SIZE, SUFFIX_COUNT]

MATCHERS = PARTS + TRAITS

PART_LABELS = {p['label'] for p in PART.get(TRAIT_STEP, [])}
SUBPART_LABELS = {s['label'] for s in SUBPART.get(TRAIT_STEP, [])}
ALL_PARTS = PART_LABELS | SUBPART_LABELS
