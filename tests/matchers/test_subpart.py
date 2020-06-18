"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestSubpart(unittest.TestCase):
    """Test the plant subpart parser."""

    def test_subpart_01(self):
        self.assertEqual(
            MATCHER.parse('terminal lobe ovate-trullate,'),
            {'subpart': [{'start': 0, 'end': 13,
                          'location': 'terminal', 'subpart': 'lobe'}],
             'plant_lobe_shape': [{'location': 'terminal',
                                   'shape': 'ovate-trullate',
                                   'start': 14, 'end': 28}]}
        )
