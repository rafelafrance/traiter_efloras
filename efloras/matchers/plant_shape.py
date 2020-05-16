"""Parse the trait."""

import regex

from .base import Base, group2span
from ..pylib.util import DotDict as Trait


class PlantShape(Base):
    """Parse plant colors."""

    def __init__(self, part):
        plant_part = f'{part}_part'
        name = f'{part}_color'

        super().__init__(name)

        self.build()

        self.replace = self.get_term_replacements()

    def convert(self, doc, match, token_map):
        """Convert the matched term into a trait."""
        trait = Trait()

        span = group2span(doc, match, 'part', token_map)
        trait.start = span.start_char
        trait.part = span.text.lower()

        return trait

    # term_matcher = {
    #     'shape': [[
    #         {'IS_DIGIT': True},
    #         {'TEXT': '-', 'OP': '?'},
    #         {'LOWER': {'IN': ['angular', 'angulate']}},
    #     ]],
    # }
    #
    # trait_matchers = {
    #     'plant_part': [[{'_': {'term': 'plant_part'}}]],
    #     'shape_phrase': [
    #         [{'_': {'term': 'shape'}}],
    #         [
    #             {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
    #             {'POS': {'IN': ['PUNCT']}},
    #             {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
    #             {'POS': {'IN': ['PUNCT']}},
    #             {'POS': {'IN': ['ADP', 'PART', 'CCONJ', ]}},
    #             {'_': {'term': {'IN': [
    #                 'shape', 'shape_starter', 'part_location']}}},
    #         ], [
    #             {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
    #             {'POS': {'IN': ['ADP', 'PART', 'CCONJ', 'PUNCT']}},
    #             {'_': {'term': {'IN': [
    #                 'shape_starter', 'part_location']}}, 'OP': '?'},
    #             {'_': {'term': {'IN': ['shape', 'part_location']}}},
    #         ], [
    #             {'_': {'term': 'shape_starter'}, 'OP': '?'},
    #             {'_': {'term': {
    #                 'IN': ['shape', 'shape_starter', 'part_location']}}},
    #             DASH,
    #             {'_': {'term': {'IN': ['shape', 'part_location']}}},
    #         ], [
    #             {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
    #             {'_': {'term': {'IN': ['shape', 'part_location']}}},
    #         ], [
    #             {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
    #             {'_': {'term': {'IN': [
    #                 'shape', 'shape_starter', 'part_location']}}},
    #             {'POS': {'IN': ['ADP', 'PART', 'CCONJ', 'PUNCT']}},
    #             {'_': {'term': 'part_location'}},
    #         ]],
    # }
    #
    # leaf_polygonal = regex.compile(r"""
    #     ( ( orbicular | angulate ) -? )?
    #     ( \b (\d-)? angular | \b (\d-)? angulate
    #         | pentagonal | pentangular | septagonal )
    #     ( -? ( orbicular | (\d-)? angulate ) )?
    #     """, regex.IGNORECASE | regex.VERBOSE)
    #
    # def parse(self, text):
    #     """Parse the traits."""
    #     traits = []
    #
    #     doc = self.find_terms(text)
    #     matches = self.get_trait_matches(doc)
    #
    #     shapes, locations = {}, {}  # Sets do not preserve order
    #     trait = Trait(start=len(text), end=0)
    #     raw_start, raw_end = len(text), 0
    #
    #     for match_id, start, end in matches:
    #         label = doc.vocab.strings[match_id]
    #         span = doc[start:end]
    #         norm = span.text.lower()
    #         trait.end = max(trait.end, span.end_char)
    #
    #         if label == 'plant_part':
    #             self.append_trait(
    #                 text, traits, trait, shapes, locations, raw_start,
    #                 raw_end)
    #             raw_start, raw_end = len(text), 0
    #             shapes, locations = {}, {}
    #             trait = Trait(
    #                 part=self.replace.get(norm, norm),
    #                 start=span.start_char,
    #                 end=span.end_char)
    #
    #         elif label == 'shape_phrase':
    #             raw_start = min(raw_start, span.start_char)
    #             raw_end = max(raw_end, span.end_char)
    #             shape = self.to_shape(span)
    #             shapes[shape] = 1
    #             locations = {**locations, **self.to_location(span)}
    #
    #     self.append_trait(
    #         text, traits, trait, shapes, locations, raw_start, raw_end)
    #
    #     return traits
    #
    # def to_shape(self, span):
    #     """Convert the span text into a shape."""
    #     words = {self.replacer(t.text): 1 for t in span
    #              if t._.term == 'shape'}
    #     return '-'.join(words.keys()) if words else ''
    #
    # def to_location(self, span):
    #     """Convert the span text into a location."""
    #     words = {self.replacer(t.text): 1 for t in span
    #              if t._.term == 'part_location'}
    #     return words
    #
    # def replacer(self, word):
    #     """Allow replace rules more complex than a dict lookup."""
    #     word = self.replace.get(word, word)
    #     word = self.leaf_polygonal.sub('polygonal', word)
    #     return word
    #
    # def append_trait(
    #         self, text, traits, trait, shapes, locations, raw_start,
    #         raw_end):
    #     """Append trait to the end of the traits list."""
    #     shapes = [self.replace.get(s, s) for s in shapes if s]
    #     if shapes:
    #         trait.raw_value = text[raw_start:raw_end]
    #         trait.value = shapes
    #         traits.append(trait)
    #         if locations:
    #             trait.location = list(locations.keys())


PLANT_SHAPE = PlantShape('plant')
CAYLX_SHAPE = PlantShape('calyx')
COROLLA_SHAPE = PlantShape('corolla')
FLOWER_SHAPE = PlantShape('flower')
HYPANTHIUM_SHAPE = PlantShape('hypanthium')
LEAF_SHAPE = PlantShape('leaf')
PETAL_SHAPE = PlantShape('petal')
PETIOLE_SHAPE = PlantShape('petiole')
SEPAL_SHAPE = PlantShape('sepal')
