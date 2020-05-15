"""Test plant count trait matcher."""

import unittest

from efloras.matchers.plant_count import PLANT_COUNT, SEPAL_COUNT
from efloras.pylib.util import DotDict as Trait


class TestPlantCount(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_plant_count_01(self):
        """It parses a simple count."""
        self.assertEqual(
            PLANT_COUNT.parse('Seeds [1–]3–12[–30]'),
            [Trait(start=0, end=19, part='seeds',
                   min_count=1, low_count=3, high_count=12, max_count=30)])

    def test_plant_count_02(self):
        """It parses a simple count range."""
        self.assertEqual(
            PLANT_COUNT.parse('Seeds 3–12'),
            [Trait(start=0, end=10, part='seeds',
                   low_count=3, high_count=12)])

    def test_plant_count_03(self):
        """It does not parse a length measurement."""
        self.assertEqual(
            PLANT_COUNT.parse('blade 5–10 × 4–9 cm'),
            [])

    def test_plant_count_04(self):
        """It does not parse a length measurement."""
        self.assertEqual(
            PLANT_COUNT.parse('petals 5, connate 1/2–2/3 length'),
            [Trait(start=0, end=8, part='petals', low_count=5)])

    def test_plant_count_05(self):
        """It handles an adverb between the plant part and counts."""
        self.assertEqual(
            PLANT_COUNT.parse('ovules mostly 120–200.'),
            [Trait(start=0, end=21, part='ovules',
                   low_count=120, high_count=200)])

    def test_plant_count_06(self):
        """It gets a sex notation."""
        self.assertEqual(
            PLANT_COUNT.parse('staminate flowers (3–)5–10(–20)'),
            [Trait(start=0, end=31, part='flowers', sex='staminate',
                   min_count=3, low_count=5,
                   high_count=10, max_count=20)])

    def test_plant_count_07(self):
        """It does not pick up a lobe notation."""
        self.assertEqual(
            PLANT_COUNT.parse('stigmas 3, 2(–3)-lobed'),
            [Trait(start=0, end=9, part='stigmas', low_count=3)])

    def test_plant_count_08(self):
        """It handles a conjunction in place of a dash."""
        self.assertEqual(
            PLANT_COUNT.parse('Petals (4 or)5,'),
            [Trait(start=0, end=14, part='petals', min_count=4, low_count=5)])

    def test_plant_count_09(self):
        """It handles a conjunction in place of a dash."""
        self.assertEqual(
            PLANT_COUNT.parse('Petals 5(or 6)'),
            [Trait(start=0, end=14, part='petals', low_count=5, max_count=6)])

    def test_plant_count_10(self):
        """It parses a sepal count."""
        self.assertEqual(
            SEPAL_COUNT.parse('Sepal [1–]3–12[–30]'),
            [Trait(start=0, end=19, part='sepal',
                   min_count=1, low_count=3, high_count=12, max_count=30)])
