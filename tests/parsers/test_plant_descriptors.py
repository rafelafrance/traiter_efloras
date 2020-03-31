"""Test the plant color trait parser."""

import unittest
from efloras.pylib.trait import Trait
from efloras.parsers.plant_descriptors import SEXUAL_DESCRIPTOR
# from efloras.parsers.plant_descriptors import SYMMETRY_DESCRIPTOR


class TestPlantColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_parse_01(self):
        """It parses a compound color notation."""
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
