"""Test the plant margin shape matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestMargin(unittest.TestCase):
    """Test the plant margin shape trait parser."""

    def test_margin_01(self):
        self.assertEqual(
            MATCHER.parse('margin shallowly undulate-crenate'),
            {'part': [{'start': 0, 'end': 6, 'part': 'margin'}],
             'margin_shape': [
                 {'start': 7, 'end': 33, 'margin_shape': 'undulate-crenate'}]}
        )

    def test_margin_02(self):
        self.assertEqual(
            MATCHER.parse(
                'margins ciliate, apex acute to long-acuminate, '
                'abaxially gland-dotted;'),
            {'part': [{'start': 0, 'end': 7, 'part': 'margin'},
                      {'start': 17, 'end': 21, 'part': 'apex'}],
             'margin_shape': [{'start': 8, 'end': 15, 'value': 'ciliate'}],
             'apex_shape': [{'margin_shape': 'acute', 'start': 22, 'end': 27},
                            {'margin_shape': 'acuminate',
                             'start': 31, 'end': 45}]}
        )
