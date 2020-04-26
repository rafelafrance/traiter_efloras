"""Test plant count trait matcher."""

import unittest

from efloras.matchers.plant_count import PLANT_COUNT
from efloras.pylib.util import DotDict as Trait


class TestPlantSize(unittest.TestCase):
    """Test plant size trait parsers."""

    def test_plant_size_01(self):
        """It parses a simple count."""
        self.assertEqual(
            PLANT_COUNT.parse('Seeds [1–]3–12[–30]'),
            [Trait(start=0, end=19, part='seeds',
                   min_count=1, low_count=3, high_count=12, max_count=30)])

    def test_plant_size_02(self):
        """It parses a simple count range."""
        self.assertEqual(
            PLANT_COUNT.parse('Seeds 3–12'),
            [Trait(start=0, end=10, part='seeds',
                   low_count=3, high_count=12)])

    def test_plant_size_03(self):
        """It does not parse a length measurement."""
        self.assertEqual(
            PLANT_COUNT.parse('blade 5–10 × 4–9 cm'),
            [])

    def test_plant_size_04(self):
        """It does not parse a length measurement."""
        self.assertEqual(
            PLANT_COUNT.parse('petals 5, connate 1/2–2/3 length'),
            [Trait(start=0, end=8, part='petals', low_count=5)])
