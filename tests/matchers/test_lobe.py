"""Test plant count trait matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestLobe(unittest.TestCase):
    """Test plant count trait matcher."""

    # def test_lobe_01(self):
    #     """It parses a simple count."""
    #     self.assertEqual(
    #         MATCHER.parse('perianth lobes elliptic, ca. 1 mm'),
    #         {'part': [{'start': 0, 'end': 8, 'value': 'perianth'}],
    #          'perianth_lobe_shape': [
    #              {'start': 0, 'end': 0, 'value': 'elliptic'}],
    #          'perianth_lobe_size': [{
    #              'start': 29, 'end': 33,
    #              'length_low': 1.0, 'length_units': 'mm'}]}
    #     )
