"""Test plant count trait matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestLobe(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_lobe_01(self):
        """It parses a simple count."""
        self.assertEqual(
            MATCHER.parse('perianth lobes elliptic, ca. 1 mm'),
            {'part': [{'start': 0, 'end': 8, 'value': 'perianth'}],
             'perianth_lobe_shape': [
                 {'start': 15, 'end': 23, 'value': 'elliptic'}],
             'perianth_lobe_size': [{
                 'start': 29, 'end': 33,
                 'length_low': 1.0, 'length_units': 'mm'}]}
        )

    def test_lobe_02(self):
        """It parses a simple count."""
        self.assertEqual(
            MATCHER.parse('fruits (1--)3-lobed,'),
            {'part': [{'start': 0, 'end': 6, 'value': 'fruit'}],
             'fruit_lobe_count': [{
                 'start': 7, 'end': 19, 'min': 1, 'low': 3}]}
        )

    def test_lobe_03(self):
        """It parses a simple count."""
        self.assertEqual(
            MATCHER.parse('petals spreading, pink, unlobed,'),
            {'part': [{'start': 0, 'end': 6, 'value': 'petal'}],
             'petal_color': [{'value': 'pink', 'start': 18, 'end': 22}],
             'petal_lobe_count': [{'start': 24, 'end': 31, 'low': 0}]}
        )