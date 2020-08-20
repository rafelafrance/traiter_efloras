"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.pylib.pipeline import trait_list


class TestPhrase(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_phrase_01(self):
        self.assertEqual(
            trait_list('Pistillate flowers  usually sessile; hypogynous'),
            [{'sex': 'female', 'part': 'flower', 'trait': 'part', 'start': 0,
              'end': 18},
             {'floral_location': 'superior',
              'sex': 'female',
              'trait': 'flower_floral_location',
              'start': 37,
              'end': 47}]
        )

    def test_phrase_02(self):
        self.assertEqual(
            trait_list('Petals glabrous, deciduous;'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'duration': 'deciduous', 'trait': 'petal_duration', 'start': 17,
              'end': 26}]
        )

    def test_phrase_03(self):
        self.assertEqual(
            trait_list('leaf blade herbaceous.'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 10},
             {'woodiness': 'herbaceous', 'trait': 'leaf_woodiness',
              'start': 11, 'end': 21}]
        )
