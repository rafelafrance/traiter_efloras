"""Test the plant descriptor matcher."""

import unittest

from efloras.matchers.plant_descriptors import PLANT_DESCRIPTOR
from efloras.pylib.trait import Trait


class TestPlantShape(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_parse_01(self):
        """It parses a compound sex notation."""
        self.assertEqual(
            PLANT_DESCRIPTOR.parse(
                'bisexual (unisexual and plants sometimes gynodioecious, '
                'or plants dioecious'),
            [
                Trait(value='bisexual', start=0, end=8),
                Trait(value='unisexual', start=10, end=19),
                Trait(value='gynodioecious', start=41, end=54),
                Trait(value='dioecious', start=66, end=75),
            ])

    def test_parse_02(self):
        """It parses a compound sex notation."""
        self.assertEqual(
            PLANT_DESCRIPTOR.parse(
                'flowers usually actinomorphic, rarely zygomorphic;'),
            [
                Trait(value='actinomorphic', start=16, end=29),
                Trait(value='zygomorphic', start=38, end=49),
            ])
