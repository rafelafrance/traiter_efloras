"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestPart(unittest.TestCase):
    """Test the plant part parser."""

    def test_part_01(self):
        self.assertEqual(
            MATCHER.parse('with thick, woody rootstock.'),
            {'rootstock_woodiness': [
                {'start': 12, 'end': 17, 'woodiness': 'woody'}],
             'part': [{'start': 18, 'end': 27, 'part': 'rootstock'}]}
        )
