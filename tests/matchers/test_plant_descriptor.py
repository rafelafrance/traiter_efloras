"""Test the plant descriptor matcher."""

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestPlantDescriptor(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_plant_descriptor_01(self):
        """It parses a compound sex notation."""
        self.assertEqual(
            MATCHER.parse(
                'bisexual (unisexual and plants sometimes gynodioecious, '
                'or plants dioecious'),
            {'reproduction': [{'value': 'bisexual', 'start': 0, 'end': 8},
                              {'value': 'unisexual', 'start': 10, 'end': 19},
                              {'value': 'gynodioecious', 'start': 41,
                               'end': 54},
                              {'value': 'dioecious', 'start': 66, 'end': 75}],
             'part': [{'start': 24, 'end': 30, 'value': 'plant'},
                      {'start': 59, 'end': 65, 'value': 'plant'}]}
        )

    def test_plant_descriptor_02(self):
        """It parses a symmetry descriptor."""
        self.assertEqual(
            MATCHER.parse(
                'flowers usually actinomorphic, rarely zygomorphic;'),
            {'part': [{'start': 0, 'end': 7, 'value': 'flower'}],
             'symmetry': [{'value': 'actinomorphic', 'start': 16, 'end': 29},
                          {'value': 'zygomorphic', 'start': 38, 'end': 49}]}
        )
