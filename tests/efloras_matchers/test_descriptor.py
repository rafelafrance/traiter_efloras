"""Test the plant descriptor matcher."""

# pylint: disable=missing-function-docstring

import unittest

from src.efloras_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestDescriptor(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_descriptor_01(self):
        self.assertEqual(
            NLP('bisexual (unisexual and plants sometimes gynodioecious, '
                'or plants dioecious'),
            [{'reproduction': 'bisexual',
              'trait': 'reproduction', 'part': 'plant',
              'start': 0,
              'end': 8},
             {'reproduction': 'unisexual',
              'trait': 'reproduction', 'part': 'plant',
              'start': 10,
              'end': 19},
             {'part': 'plant', 'trait': 'part', 'start': 24, 'end': 30},
             {'reproduction': 'gynodioecious',
              'trait': 'reproduction', 'part': 'plant',
              'start': 41,
              'end': 54},
             {'part': 'plant', 'trait': 'part', 'start': 59, 'end': 65},
             {'reproduction': 'dioecious',
              'trait': 'reproduction', 'part': 'plant',
              'start': 66,
              'end': 75}]
        )

    def test_descriptor_02(self):
        self.assertEqual(
            NLP('Shrubs , to 1.5 m, forming rhizomatous colonies.'),
            [{'habit': 'shrub', 'trait': 'habit', 'part': 'plant',
              'start': 0, 'end': 6},
             {'length_high': 1.5, 'length_units': 'm',
              'trait': 'size', 'part': 'plant',
              'start': 9, 'end': 17}]
        )

    def test_descriptor_03(self):
        self.assertEqual(
            NLP('Stems often caespitose'),
            [{'part': 'stem', 'trait': 'part', 'start': 0, 'end': 5},
             {'habit': 'cespitose', 'trait': 'habit', 'part': 'plant',
              'start': 12, 'end': 22}]
        )

    def test_descriptor_04(self):
        self.assertEqual(
            NLP('Herbs perennial or subshrubs, epiphytic or epilithic.'),
            [{'woodiness': 'herbaceous', 'trait': 'woodiness', 'part': 'plant',
              'start': 0, 'end': 5},
             {'plant_duration': 'perennial',
              'trait': 'plant_duration', 'part': 'plant',
              'start': 6, 'end': 15},
             {'habit': 'shrub', 'trait': 'habit',
              'part': 'plant', 'start': 19, 'end': 28},
             {'habitat': 'epiphytic', 'trait': 'habitat',
              'part': 'plant', 'start': 30, 'end': 39},
             {'habitat': 'epilithic', 'trait': 'habitat',
              'part': 'plant', 'start': 43, 'end': 52}]
        )
