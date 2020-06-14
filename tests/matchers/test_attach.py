"""Test attaching traits to plant parts."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestAttach(unittest.TestCase):
    """Test attaching traits to plant parts."""

    def test_attach_01(self):
        self.assertEqual(
            MATCHER.parse(
                'keel with blue tip; standard 8-9 × ca. 6 mm, '
                'widely elliptic, emarginate; wings'),
            {'part': [{'start': 0, 'end': 4, 'value': 'keel'},
                      {'start': 74, 'end': 79, 'value': 'wing'}],
             'keel_color': [{'value': 'blue-tip', 'start': 10, 'end': 18}],
             'keel_size': [{'start': 39, 'end': 43,
                            'length_low': 6, 'length_units': 'mm'}],
             'keel_shape': [{'value': 'elliptic', 'start': 52, 'end': 60},
                            {'value': 'emarginate', 'start': 62, 'end': 72}]}
        )
