"""A list of all matchers."""
from .color import COLOR
from .count import COUNT
from .descriptor import DESCRIPTOR
from .habit import HABIT
from .margin import MARGIN_SHAPE
from .part import PART
from .phrase import PHRASE
from .range import RANGE
from .shape import SHAPE
from .size import SIZE
from .subpart import SUBPART
from .suffix_count import SUFFIX_COUNT

PARTS = [PART, SUBPART]
TRAITS = [
    COLOR, COUNT, DESCRIPTOR, HABIT, MARGIN_SHAPE, PHRASE, RANGE,
    SHAPE, SIZE, SUFFIX_COUNT]

MATCHERS = PARTS + TRAITS

PART_NAMES = {p['name'] for p in PARTS}
ALL_PART_LABELS = {m['label'] for p in PARTS for m in p.get('matchers', [])}
PART_LABELS = {p['label'] for p in PART.get('matchers', [])}
SUBPART_LABELS = {s['label'] for s in SUBPART.get('matchers', [])}

TRAIT_NAMES = {t['name'] for t in TRAITS}
TRAIT_LABELS = {m['label'] for t in TRAITS for m in t.get('matchers', [])}

GROUP_LABELS = {g['label'] for m in MATCHERS for g in m.get('groupers', [])}
