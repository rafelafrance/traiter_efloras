"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from tests.setup import test


class TestPhrase(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_phrase_01(self):
        self.assertEqual(
            test('Pistillate flowers usually sessile; hypogynous'),
            [{'sex': 'female', 'part': 'flower', 'trait': 'part', 'start': 0,
              'end': 18},
             {'floral_location': 'superior', 'sex': 'female', 'part': 'flower',
              'trait': 'floral_location', 'start': 36, 'end': 46}]
        )

    def test_phrase_02(self):
        self.assertEqual(
            test('Petals glabrous, deciduous;'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'duration': 'deciduous', 'trait': 'duration',
              'part': 'plant', 'start': 17, 'end': 26}]
        )

    def test_phrase_03(self):
        self.assertEqual(
            test('leaf blade herbaceous.'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 10},
             {'woodiness': 'herbaceous', 'trait': 'woodiness',
              'part': 'plant', 'start': 11, 'end': 21}]
        )
