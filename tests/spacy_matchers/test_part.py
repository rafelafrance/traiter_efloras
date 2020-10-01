"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestPart(unittest.TestCase):
    """Test the plant part parser."""

    def test_part_01(self):
        self.assertEqual(
            NLP('with thick, woody rootstock.'),
            [{'woodiness': 'woody', 'trait': 'woodiness', 'part': 'rootstock',
              'start': 12, 'end': 17},
             {'part': 'rootstock', 'trait': 'part', 'start': 18, 'end': 27}]
        )

    def test_part_02(self):
        self.assertEqual(
            NLP('leaflets mostly 1 or 3'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'low': 1, 'high': 3, 'trait': 'count', 'part': 'leaflet',
              'start': 16, 'end': 22}]
        )

    def test_part_03(self):
        self.assertEqual(
            NLP('Receptacle discoid.'),
            []
        )

    def test_part_04(self):
        self.assertEqual(
            NLP('Flowers: sepals (pistillate)'),
            [{'part': 'flower', 'trait': 'part', 'start': 0, 'end': 7},
             {'part': 'sepal', 'sex': 'female',
              'trait': 'part', 'start': 9, 'end': 28}]
        )

    def test_part_05(self):
        self.assertEqual(
            NLP('Flowers: sepals (pistillate)'),
            [{'part': 'flower', 'trait': 'part', 'start': 0, 'end': 7},
             {'part': 'sepal', 'sex': 'female',
              'trait': 'part', 'start': 9, 'end': 28}]
        )

    def test_part_06(self):
        self.assertEqual(
            NLP('Flowers: staminate:'),
            [{'part': 'flower', 'sex': 'male',
              'trait': 'part', 'start': 0, 'end': 18}]
        )
