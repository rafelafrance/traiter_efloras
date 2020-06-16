"""Test attaching traits to plant parts."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.util import shorten

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestAttach(unittest.TestCase):
    """Test attaching traits to plant parts."""

    def test_attach_01(self):
        self.assertEqual(
            MATCHER.parse(
                'keel with blue tip; standard 8-9 × ca. 6 mm, '
                'widely elliptic, emarginate; wings'),
            {'subpart': [{'subpart': 'keel', 'start': 0, 'end': 4}],
             'wing_keel_color': [
                 {'color': 'blue-tip', 'start': 10, 'end': 18}],
             'wing_keel_size': [{'start': 39, 'end': 43,
                                 'length_low': 6, 'length_units': 'mm'}],
             'wing_keel_shape': [{'shape': 'elliptic', 'start': 52, 'end': 60},
                                 {'shape': 'emarginate', 'start': 62,
                                  'end': 72}],
             'part': [{'start': 74, 'end': 79, 'part': 'wing'}]}
        )

    def test_attach_02(self):
        self.assertEqual(
            MATCHER.parse(shorten("""
                Calyx ca. 5 mm, loosely to rather densely appressed hairy;
                teeth ca. 2.5 mm.
                """)),
            {'part': [{'start': 0, 'end': 5, 'part': 'calyx'}],
             'calyx_size': [{'start': 10, 'end': 14,
                             'length_low': 5, 'length_units': 'mm'}],
             'subpart': [{'subpart': 'tooth', 'start': 59, 'end': 64}],
             'calyx_tooth_size': [{'start': 69, 'end': 75,
                                   'length_low': 2.5, 'length_units': 'mm'}]}
        )
