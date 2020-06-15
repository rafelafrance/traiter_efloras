"""Test plant count trait matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestSuffixCount(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_suffix_count_01(self):
        self.assertEqual(
            MATCHER.parse('perianth lobes elliptic, ca. 1 mm'),
            {'part': [{'start': 0, 'end': 8, 'part': 'perianth'}],
             'subpart': [{'subpart': 'lobe', 'start': 9, 'end': 14}],
             'perianth_lobe_shape': [
                 {'shape': 'elliptic', 'start': 15, 'end': 23}],
             'perianth_lobe_size': [{'start': 29, 'end': 33,
                                     'length_low': 1, 'length_units': 'mm'}]}
        )

    def test_suffix_count_02(self):
        self.assertEqual(
            MATCHER.parse('fruits (1--)3-lobed,'),
            {'part': [{'start': 0, 'end': 6, 'part': 'fruit'}],
             'fruit_lobe_count': [{
                 'start': 7, 'end': 19, 'min': 1, 'low': 3}]}
        )

    def test_suffix_count_03(self):
        self.assertEqual(
            MATCHER.parse('petals spreading, pink, unlobed,'),
            {'part': [{'start': 0, 'end': 6, 'part': 'petal'}],
             'petal_color': [{'color': 'pink', 'start': 18, 'end': 22}],
             'petal_lobe_count': [{'start': 24, 'end': 31, 'low': 0}]}
        )

    def test_suffix_count_04(self):
        self.assertEqual(
            MATCHER.parse('Inflorescences 10+-flowered'),
            {'part': [{'start': 0, 'end': 14, 'part': 'inflorescence'}],
             'inflorescence_flower_count': [
                 {'start': 15, 'end': 27, 'low': 10, 'indefinite': True}]}
        )
