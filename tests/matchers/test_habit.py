"""Test the plant habit matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestHabit(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_habit_01(self):
        self.assertEqual(
            MATCHER.parse('Shrubs , to 1.5 m, forming rhizomatous colonies.'),
            {'plant_habit': [{'habit': 'shrub', 'start': 0, 'end': 6}],
             'plant_size': [{'start': 9, 'end': 17,
                             'length_high': 1.5, 'length_units': 'm'}]}
        )

    def test_habit_02(self):
        self.assertEqual(
            MATCHER.parse('Stems often caespitose'),
            {'part': [{'start': 0, 'end': 5, 'part': 'stem'}],
             'plant_habit_shape': [
                 {'habit': 'cespitose', 'start': 12, 'end': 22}]}
        )

    def test_habit_03(self):
        self.assertEqual(
            MATCHER.parse('Herbs perennial or subshrubs, epiphytic '
                          'or epilithic.'),
            {
                'plant_woodiness': [
                    {'habit': 'herbaceous', 'start': 0, 'end': 5}],
                'plant_life_span': [
                    {'descriptor': 'perennial', 'start': 6, 'end': 15}],
                'plant_habit': [{'habit': 'shrub', 'start': 19, 'end': 28}],
                'plant_habitat': [
                    {'habit': 'epiphytic', 'start': 30, 'end': 39},
                    {'habit': 'epilithic', 'start': 43, 'end': 52}]}
        )

    def test_habit_04(self):
        self.assertEqual(
            MATCHER.parse('leaf blade herbaceous.'),
            {'part': [{'start': 0, 'end': 10, 'part': 'leaf'}],
             'plant_woodiness': [
                 {'habit': 'herbaceous', 'start': 11, 'end': 21}]}
        )
