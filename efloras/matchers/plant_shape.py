"""Parse the trait."""
import regex
from spacy.matcher import Matcher

from .base import Base
from ..pylib.terms import DASH, replacements
from ..pylib.util import DotDict as Trait


class PlantShape(Base):
    """Parse plant colors."""

    term_matcher = {
        'shape': [[
            {'IS_DIGIT': True},
            {'TEXT': '-', 'OP': '?'},
            {'LOWER': {'IN': ['angular', 'angulate']}},
        ]],
    }

    trait_matchers = {
        'plant_part': [[{'_': {'term': 'plant_part'}}]],
        'shape_phrase': [
            [{'_': {'term': 'shape'}}],
            [
                {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
                {'POS': {'IN': ['PUNCT']}},
                {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
                {'POS': {'IN': ['PUNCT']}},
                {'POS': {'IN': ['ADP', 'PART', 'CCONJ', ]}},
                {'_': {'term': {'IN': [
                    'shape', 'shape_starter', 'part_location']}}},
            ], [
                {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
                {'POS': {'IN': ['ADP', 'PART', 'CCONJ', 'PUNCT']}},
                {'_': {'term': {'IN': [
                    'shape_starter', 'part_location']}}, 'OP': '?'},
                {'_': {'term': {'IN': ['shape', 'part_location']}}},
            ], [
                {'_': {'term': 'shape_starter'}, 'OP': '?'},
                {'_': {'term': {
                    'IN': ['shape', 'shape_starter', 'part_location']}}},
                DASH,
                {'_': {'term': {'IN': ['shape', 'part_location']}}},
            ], [
                {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
                {'_': {'term': {'IN': ['shape', 'part_location']}}},
            ], [
                {'_': {'term': {'IN': ['shape_starter', 'part_location']}}},
                {'_': {'term': {'IN': [
                    'shape', 'shape_starter', 'part_location']}}},
                {'POS': {'IN': ['ADP', 'PART', 'CCONJ', 'PUNCT']}},
                {'_': {'term': 'part_location'}},
            ]],
    }

    leaf_polygonal = regex.compile(r"""
        ( ( orbicular | angulate ) -? )?
        ( \b (\d-)? angular | \b (\d-)? angulate
            | pentagonal | pentangular | septagonal )
        ( -? ( orbicular | (\d-)? angulate ) )?
        """, regex.IGNORECASE | regex.VERBOSE)

    def __init__(self):
        super().__init__('plant_shape')

        matcher = Matcher(self.nlp.vocab)
        _ = [matcher.add(k, v, on_match=self.term_label)
             for k, v in self.term_matcher.items()]
        self.term_matchers.append(matcher)
        self.replace = replacements(self.name)

    def parse(self, text):
        """Parse the traits."""
        traits = []

        doc = self.find_terms(text)
        matches = self.get_trait_matches(doc)

        shapes, locations = {}, {}  # Sets do not preserve order
        trait = Trait(start=len(text), end=0)
        raw_start, raw_end = len(text), 0

        for match_id, start, end in matches:
            label = doc.vocab.strings[match_id]
            span = doc[start:end]
            norm = span.text.lower()
            trait.end = max(trait.end, span.end_char)

            if label == 'plant_part':
                self.append_trait(
                    text, traits, trait, shapes, locations, raw_start, raw_end)
                raw_start, raw_end = len(text), 0
                shapes, locations = {}, {}
                trait = Trait(
                    part=self.replace.get(norm, norm),
                    start=span.start_char,
                    end=span.end_char)

            elif label == 'shape_phrase':
                raw_start = min(raw_start, span.start_char)
                raw_end = max(raw_end, span.end_char)
                shape = self.to_shape(span)
                shapes[shape] = 1
                locations = {**locations, **self.to_location(span)}

        self.append_trait(
            text, traits, trait, shapes, locations, raw_start, raw_end)

        return traits

    def to_shape(self, span):
        """Convert the span text into a shape."""
        words = {self.replacer(t.text): 1 for t in span
                 if t._.term == 'shape'}
        return '-'.join(words.keys()) if words else ''

    def to_location(self, span):
        """Convert the span text into a location."""
        words = {self.replacer(t.text): 1 for t in span
                 if t._.term == 'part_location'}
        return words

    def replacer(self, word):
        """Allow replace rules more complex than a dict lookup."""
        word = self.replace.get(word, word)
        word = self.leaf_polygonal.sub('polygonal', word)
        return word

    def append_trait(
            self, text, traits, trait, shapes, locations, raw_start, raw_end):
        """Append trait to the end of the traits list."""
        shapes = [self.replace.get(s, s) for s in shapes if s]
        if shapes:
            trait.raw_value = text[raw_start:raw_end]
            trait.value = shapes
            traits.append(trait)
            if locations:
                trait.location = list(locations.keys())


PLANT_SHAPE = PlantShape()
