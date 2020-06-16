"""Test the plant descriptor matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestDescriptor(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_descriptor_01(self):
        self.assertEqual(
            MATCHER.parse(
                'bisexual (unisexual and plants sometimes gynodioecious, '
                'or plants dioecious'),
            {
                'plant_reproduction': [
                    {'reproduction': 'bisexual', 'start': 0, 'end': 8},
                    {'reproduction': 'unisexual', 'start': 10, 'end': 19},
                    {'reproduction': 'gynodioecious', 'start': 41, 'end': 54},
                    {'reproduction': 'dioecious', 'start': 66, 'end': 75}],
                'part': [
                    {'start': 24, 'end': 30, 'part': 'plant'},
                    {'start': 59, 'end': 65, 'part': 'plant'}]}
        )

    def test_descriptor_02(self):
        self.assertEqual(
            MATCHER.parse('Shrubs , to 1.5 m, forming rhizomatous colonies.'),
            {'plant_habit': [{'habit': 'shrub', 'start': 0, 'end': 6}],
             'plant_size': [{'start': 9, 'end': 17,
                             'length_high': 1.5, 'length_units': 'm'}]}
        )

    def test_descriptor_03(self):
        self.assertEqual(
            MATCHER.parse('Stems often caespitose'),
            {'part': [{'start': 0, 'end': 5, 'part': 'stem'}],
             'plant_habit_shape': [
                 {'habit_shape': 'cespitose', 'start': 12, 'end': 22}]}
        )

    def test_descriptor_04(self):
        self.assertEqual(
            MATCHER.parse('Herbs perennial or subshrubs, epiphytic '
                          'or epilithic.'),
            {
                'plant_woodiness': [
                    {'woodiness': 'herbaceous', 'start': 0, 'end': 5}],
                'plant_duration': [
                    {'plant_duration': 'perennial', 'start': 6, 'end': 15}],
                'plant_habit': [{'habit': 'shrub', 'start': 19, 'end': 28}],
                'plant_habitat': [
                    {'habitat': 'epiphytic', 'start': 30, 'end': 39},
                    {'habitat': 'epilithic', 'start': 43, 'end': 52}]}
        )

    def test_descriptor_05(self):
        self.assertEqual(
            MATCHER.parse('leaf blade herbaceous.'),
            {'part': [{'start': 0, 'end': 10, 'part': 'leaf'}],
             'plant_woodiness': [
                 {'woodiness': 'herbaceous', 'start': 11, 'end': 21}]}
        )
