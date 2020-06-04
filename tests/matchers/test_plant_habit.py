"""Test the plant habit matcher."""

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestPlantHabit(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_plant_habit_01(self):
        """It parses a compound sex notation."""
        self.assertEqual(
            MATCHER.parse(
                'Shrubs , to 1.5 m, forming rhizomatous colonies.'),
            {'habit': [{'value': 'shrub', 'start': 0, 'end': 6}],
             'plant_size': [{'start': 9, 'end': 17,
                             'length_high': 1.5, 'length_units': 'm'}]}
        )
