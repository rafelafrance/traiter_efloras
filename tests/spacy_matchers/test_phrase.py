"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from src.spacy_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestPhrase(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_phrase_01(self):
        self.assertEqual(
            NLP('Pistillate flowers  usually sessile; hypogynous'),
            [{'sex': 'female', 'part': 'flower', 'trait': 'part', 'start': 0,
              'end': 18},
             {'floral_location': 'superior', 'sex': 'female', 'part': 'flower',
              'trait': 'floral_location', 'start': 37, 'end': 47}]
        )

    def test_phrase_02(self):
        self.assertEqual(
            NLP('Petals glabrous, deciduous;'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'duration': 'deciduous', 'trait': 'duration',
              'part': 'petal', 'start': 17, 'end': 26}]
        )

    def test_phrase_03(self):
        self.assertEqual(
            NLP('leaf blade herbaceous.'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 10},
             {'woodiness': 'herbaceous', 'trait': 'woodiness',
              'part': 'leaf', 'start': 11, 'end': 21}]
        )
