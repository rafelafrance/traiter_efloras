"""Test the plant color trait parser."""

import unittest

from efloras.parsers.plant_descriptor import SEXUAL_DESCRIPTOR, \
    SYMMETRY_DESCRIPTOR
from efloras.pylib.trait import Trait


class TestPlantDescriptor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_parse_01(self):
        """It parses a compound sex notation."""
        self.assertEqual(
            SEXUAL_DESCRIPTOR.parse(
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
            SYMMETRY_DESCRIPTOR.parse(
                'flowers usually actinomorphic, rarely zygomorphic;'),
            [
                Trait(value='actinomorphic', start=16, end=29),
                Trait(value='zygomorphic', start=38, end=49),
            ])
