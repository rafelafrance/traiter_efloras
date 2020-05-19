"""Test the plant descriptor matcher."""

import unittest

from efloras.matchers.base import Base


class TestPlantDescriptor(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_plant_descriptor_01(self):
        """It parses a compound sex notation."""
        self.assertEqual(
            Base('sexual_descriptor').parse(
                'bisexual (unisexual and plants sometimes gynodioecious, '
                'or plants dioecious'),
            [{'sexual_descriptor': [{'value': 'bisexual',
                                     'category': 'sexual_descriptor',
                                     'start': 0, 'end': 8,
                                     'raw_value': 'bisexual'},
                                    {'value': 'unisexual',
                                     'category': 'sexual_descriptor',
                                     'start': 10, 'end': 19,
                                     'raw_value': 'unisexual'},
                                    {'value': 'gynodioecious',
                                     'category': 'sexual_descriptor',
                                     'start': 41, 'end': 54,
                                     'raw_value': 'gynodioecious'},
                                    {'value': 'dioecious',
                                     'category': 'sexual_descriptor',
                                     'start': 66, 'end': 75,
                                     'raw_value': 'dioecious'}]}]
        )

    def test_plant_descriptor_02(self):
        """It parses a symmetry descriptor."""
        self.assertEqual(
            Base('symmetry_descriptor').parse(
                'flowers usually actinomorphic, rarely zygomorphic;'),
            [{'symmetry_descriptor': [{'value': 'actinomorphic',
                                       'category': 'symmetry_descriptor',
                                       'start': 16, 'end': 29,
                                       'raw_value': 'actinomorphic'},
                                      {'value': 'zygomorphic',
                                       'category': 'symmetry_descriptor',
                                       'start': 38, 'end': 49,
                                       'raw_value': 'zygomorphic'}]},
             {'part': [{'value': 'flower', 'start': 0, 'end': 7,
                        'raw_value': 'flowers'}]}]
        )
