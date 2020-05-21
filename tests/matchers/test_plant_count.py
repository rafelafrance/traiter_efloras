"""Test plant count trait matcher."""

import unittest

from efloras.matchers.matcher import Matcher


class TestPlantCount(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_plant_count_01(self):
        """It parses a simple count."""
        self.assertEqual(
            Matcher('*_count').parse('Seeds [1–]3–12[–30]'),
            [{'part': [
                {'value': 'seed', 'start': 0, 'end': 5, 'raw_value': 'Seeds'}],
                'seed_count': [{'start': 6,
                                'end': 19,
                                'raw_value': '[1–]3–12[–30]',
                                'value': {'min_count': 1,
                                          'low_count': 3,
                                          'high_count': 12,
                                          'max_count': 30}}]}]
        )

    def test_plant_count_02(self):
        """It parses a seed count."""
        self.assertEqual(
            Matcher('*_count').parse('Seeds 3–12'),
            [{'part': [
                {'value': 'seed', 'start': 0, 'end': 5, 'raw_value': 'Seeds'}],
                'seed_count': [{'start': 6,
                                'end': 10,
                                'raw_value': '3–12',
                                'value': {'low_count': 3, 'high_count': 12}}]}]
        )

    def test_plant_count_03(self):
        """It does not parse a length measurement."""
        self.assertEqual(
            Matcher('*_count').parse('blade 5–10 × 4–9 cm'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 5,
                        'raw_value': 'blade'}]}]
        )

    def test_plant_count_04(self):
        """It does not parse a length measurement."""
        self.assertEqual(
            Matcher('*_count').parse('petals 5, connate 1/2–2/3 length'),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 6,
                        'raw_value': 'petals'}]}]
        )

    def test_plant_count_05(self):
        """It handles ovary counts."""
        self.assertEqual(
            Matcher('*_count').parse('ovules mostly 120–200.'),
            [{'part': [{'value': 'ovary', 'start': 0, 'end': 6,
                        'raw_value': 'ovules'}],
              'ovary_count': [{'start': 14,
                               'end': 21,
                               'raw_value': '120–200',
                               'value': {'low_count': 120,
                                         'high_count': 200}}]}]
        )

    def test_plant_count_06(self):
        """We're not counting flowers yet."""
        self.assertEqual(
            Matcher('*_count').parse('staminate flowers (3–)5–10(–20)'),
            [{'part': [{'value': 'flower',
                        'start': 0, 'end': 17,
                        'raw_value': 'staminate flowers',
                        'sex': 'staminate'}]}]
        )

    def test_plant_count_07(self):
        """It handles an ovary."""
        self.assertEqual(
            Matcher('ovary_count').parse('Ovaries (4 or)5,'),
            [{'part': [{'value': 'ovary', 'start': 0, 'end': 7,
                        'raw_value': 'Ovaries'}],
              'ovary_count': [{'start': 8,
                               'end': 15,
                               'raw_value': '(4 or)5',
                               'value': {'min_count': 4, 'low_count': 5}}]}]
        )

    def test_plant_count_08(self):
        """It handles a conjunction in place of a dash."""
        self.assertEqual(
            Matcher('seed_count').parse('Seeds 5(or 6)'),
            [{'part': [
                {'value': 'seed', 'start': 0, 'end': 5, 'raw_value': 'Seeds'}],
                'seed_count': [{'start': 6,
                                'end': 13,
                                'raw_value': '5(or 6)',
                                'value': {'low_count': 5, 'max_count': 6}}]}]
        )

    def test_plant_count_09(self):
        """It parses a sepal count."""
        self.assertEqual(
            Matcher('stamen_count').parse('Stamen [1–]3–12[–30]'),
            [{'part': [{'value': 'stamen', 'start': 0, 'end': 6,
                        'raw_value': 'Stamen'}],
              'stamen_count': [{'start': 7,
                                'end': 20,
                                'raw_value': '[1–]3–12[–30]',
                                'value': {'min_count': 1,
                                          'low_count': 3,
                                          'high_count': 12,
                                          'max_count': 30}}]}]
        )
