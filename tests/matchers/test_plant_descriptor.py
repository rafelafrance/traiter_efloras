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
            [{'plant_sex': [
                {'value': 'bisexual', 'start': 0, 'end': 8},
                {'value': 'unisexual', 'start': 10, 'end': 19},
                {'value': 'gynodioecious', 'start': 41, 'end': 54},
                {'value': 'dioecious', 'start': 66, 'end': 75}]},
             {'part': [{'value': 'plant', 'start': 24, 'end': 30}]},
             {'part': [{'value': 'plant', 'start': 59, 'end': 65}]}]
        )

    def test_plant_descriptor_02(self):
        """It parses a symmetry descriptor."""
        self.assertEqual(
            MATCHER.parse(
                'flowers usually actinomorphic, rarely zygomorphic;'),
            [{'symmetry': [
                {'value': 'actinomorphic', 'start': 16, 'end': 29},
                {'value': 'zygomorphic', 'start': 38, 'end': 49}]},
             {'part': [{'value': 'flower', 'start': 0, 'end': 7}]}]
        )
