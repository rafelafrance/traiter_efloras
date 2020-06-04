"""Test plant count trait matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestCount(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_count_01(self):
        """It parses a simple count."""
        self.assertEqual(
            MATCHER.parse('Seeds [1–]3–12[–30]'),
            {'part': [{'start': 0, 'end': 5, 'value': 'seed'}],
             'seed_count': [{'start': 6, 'end': 19,
                             'min': 1, 'low': 3, 'high': 12, 'max': 30}]}
        )

    def test_count_02(self):
        """It parses a seed count."""
        self.assertEqual(
            MATCHER.parse('Seeds 3–12'),
            {'part': [{'start': 0, 'end': 5, 'value': 'seed'}],
             'seed_count': [{'start': 6, 'end': 10, 'low': 3, 'high': 12}]}
        )

    def test_count_03(self):
        """It does not parse a length measurement."""
        self.assertEqual(
            MATCHER.parse('blade 5–10 × 4–9 cm'),
            {'part': [{'start': 0, 'end': 5, 'value': 'leaf'}],
             'leaf_size': [{'start': 6, 'end': 19,
                            'length_low': 5.0, 'length_high': 10.0,
                            'width_low': 4.0, 'width_high': 9.0,
                            'width_units': 'cm'}]}
        )

    def test_count_04(self):
        """It does not parse a length measurement."""
        self.assertEqual(
            MATCHER.parse('petals 5, connate 1/2–2/3 length'),
            {'part': [{'start': 0, 'end': 6, 'value': 'petal'}],
             'petal_count': [{'start': 7, 'end': 8, 'low': 5}]}
        )

    def test_count_05(self):
        self.assertEqual(
            MATCHER.parse('ovules mostly 120–200.'),
            {'part': [{'start': 0, 'end': 6, 'value': 'ovary'}],
             'ovary_count': [
                 {'start': 14, 'end': 21, 'low': 120, 'high': 200}]}
        )

    def test_count_06(self):
        self.assertEqual(
            MATCHER.parse('Staminate flowers (3–)5–10(–20)'),
            {'part': [
                {'start': 0, 'end': 17, 'sex': 'male', 'value': 'flower'}],
             'flower_count': [{'start': 18, 'end': 31,
                               'min': 3, 'low': 5,
                               'high': 10, 'max': 20,
                               'sex': 'male'}]}
        )

    def test_count_07(self):
        self.assertEqual(
            MATCHER.parse('Ovaries (4 or)5,'),
            {'part': [{'start': 0, 'end': 7, 'value': 'ovary'}],
             'ovary_count': [{'start': 8, 'end': 15, 'min': 4, 'low': 5}]}
        )

    def test_count_08(self):
        self.assertEqual(
            MATCHER.parse('Seeds 5(or 6)'),
            {'part': [{'start': 0, 'end': 5, 'value': 'seed'}],
             'seed_count': [{'start': 6, 'end': 13, 'low': 5, 'max': 6}]}
        )

    def test_count_09(self):
        """It parses a sepal count."""
        self.assertEqual(
            MATCHER.parse('Stamen [1–]3–12[–30]'),
            {'part': [{'start': 0, 'end': 6, 'value': 'stamen'}],
             'stamen_count': [{'start': 7, 'end': 20,
                               'min': 1, 'low': 3, 'high': 12, 'max': 30}]}
        )

    def test_count_10(self):
        """Units are required."""
        self.assertEqual(
            MATCHER.parse('leaf (12-)23-34 × 45-56'),
            {'part': [{'value': 'leaf', 'start': 0, 'end': 4}]}
        )

    def test_count_11(self):
        """Units are required."""
        self.assertEqual(
            MATCHER.parse('stigma papillose on 1 side,'),
            {'part': [{'value': 'stigma', 'start': 0, 'end': 6}]}
        )

    def test_count_12(self):
        self.assertEqual(
            MATCHER.parse('Male flowers with 2-8(-20) stamens;'),
            {'part': [
                {'start': 0, 'end': 12, 'sex': 'male', 'value': 'flower'},
                {'sex': 'male', 'start': 27, 'end': 34, 'value': 'stamen'}],
             'stamen_count': [{'sex': 'male', 'start': 18, 'end': 26,
                               'low': 2, 'high': 8, 'max': 20}]}
        )

    def test_count_13(self):
        self.assertEqual(
            MATCHER.parse('Male flowers with 2-8(-20) stamens;'),
            {'part': [
                {'start': 0, 'end': 12, 'sex': 'male', 'value': 'flower'},
                {'sex': 'male', 'start': 27, 'end': 34, 'value': 'stamen'}],
             'stamen_count': [{'sex': 'male', 'start': 18, 'end': 26,
                               'low': 2, 'high': 8, 'max': 20}]}
        )

    def test_count_14(self):
        self.assertEqual(
            MATCHER.parse('leaflets in 3 or 4 pairs,'),
            {'part': [{'start': 0, 'end': 8, 'value': 'leaf'}],
             'leaf_count': [
                 {'start': 12, 'end': 24, 'low': 3, 'high': 4, 'as': 'pairs'}]}
        )
