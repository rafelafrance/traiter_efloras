"""Test the plant color ruler."""

import unittest
from efloras.pylib.trait import Trait
from efloras.rulers.plant_color import HYPANTHIUM_COLOR


class TestPlantColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_parse_01(self):
        """It parses a compound color notation."""
        self.assertEqual(
            HYPANTHIUM_COLOR.parse(
                'hypanthium green or greenish yellow, '
                'usually not purple-spotted, rarely purple-spotted distally'),
            [Trait(start=0, end=86, part='hypanthium',
                   value=['green', 'green-yellow', 'purple-spotted'],
                   raw_value='green or greenish yellow, usually not '
                             'purple-spotted, rarely purple-spotted')])
