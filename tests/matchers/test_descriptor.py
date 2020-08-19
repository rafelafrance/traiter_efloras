"""Test the plant descriptor matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.pylib.pipeline import parse


class TestDescriptor(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_descriptor_01(self):
        self.assertEqual(
            parse(
                'bisexual (unisexual and plants sometimes gynodioecious, '
                'or plants dioecious'),
            [{'reproduction': 'bisexual',
              'trait': 'plant_reproduction',
              'start': 0,
              'end': 8},
             {'reproduction': 'unisexual',
              'trait': 'plant_reproduction',
              'start': 10,
              'end': 19},
             {'part': 'plant', 'trait': 'part', 'start': 24, 'end': 30},
             {'reproduction': 'gynodioecious',
              'trait': 'plant_reproduction',
              'start': 41,
              'end': 54},
             {'part': 'plant', 'trait': 'part', 'start': 59, 'end': 65},
             {'reproduction': 'dioecious',
              'trait': 'plant_reproduction',
              'start': 66,
              'end': 75}]
        )

    def test_descriptor_02(self):
        self.assertEqual(
            parse('Shrubs , to 1.5 m, forming rhizomatous colonies.'),
            [{'habit': 'shrub', 'trait': 'plant_habit', 'start': 0, 'end': 6},
             {'length_high': 1.5,
              'length_units': 'm',
              'trait': 'plant_size',
              'start': 9,
              'end': 17}]
        )

    def test_descriptor_03(self):
        self.assertEqual(
            parse('Stems often caespitose'),
            [{'part': 'stem', 'trait': 'part', 'start': 0, 'end': 5},
             {'habit_shape': 'cespitose',
              'trait': 'plant_habit_shape',
              'start': 12,
              'end': 22}]
        )

    def test_descriptor_04(self):
        self.assertEqual(
            parse('Herbs perennial or subshrubs, epiphytic or epilithic.'),
            [{'woodiness': 'herbaceous', 'trait': 'plant_woodiness',
              'start': 0, 'end': 5},
             {'plant_duration': 'perennial', 'trait': 'plant_duration',
              'start': 6, 'end': 15},
             {'habit': 'shrub', 'trait': 'plant_habit', 'start': 19,
              'end': 28},
             {'habitat': 'epiphytic', 'trait': 'plant_habitat', 'start': 30,
              'end': 39},
             {'habitat': 'epilithic', 'trait': 'plant_habitat', 'start': 43,
              'end': 52}]
        )
