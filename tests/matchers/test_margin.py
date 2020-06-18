"""Test the plant margin shape matcher."""

# pylint: disable=missing-function-docstring

import unittest

from traiter.util import shorten

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestMargin(unittest.TestCase):
    """Test the plant margin shape trait parser."""

    def test_margin_01(self):
        self.assertEqual(
            MATCHER.parse('margin shallowly undulate-crenate'),
            {'subpart': [{'subpart': 'margin', 'start': 0, 'end': 6}],
             'plant_margin_shape': [{'start': 7, 'end': 33,
                                     'margin_shape': 'undulate-crenate'}]}
        )

    def test_margin_02(self):
        self.assertEqual(
            MATCHER.parse(
                'margins ciliate, apex acute to long-acuminate,'),
            {'subpart': [{'subpart': 'margin', 'start': 0, 'end': 7},
                         {'subpart': 'apex', 'start': 17, 'end': 21}],
             'plant_margin_shape': [
                 {'start': 8, 'end': 15, 'margin_shape': 'ciliate'}],
             'plant_apex_shape': [{'shape': 'acute', 'start': 22, 'end': 27},
                                  {'shape': 'acuminate', 'start': 31,
                                   'end': 45}]}
        )

    def test_margin_03(self):
        self.assertEqual(
            MATCHER.parse('reniform, undulate-margined'),
            {'plant_shape': [{'shape': 'reniform', 'start': 0, 'end': 8}],
             'plant_margin_shape': [
                 {'start': 10, 'end': 27, 'margin_shape': 'undulate'}]}
        )

    def test_margin_04(self):
        self.assertEqual(
            MATCHER.parse('margins thickened-corrugated'),
            {'subpart': [{'subpart': 'margin', 'start': 0, 'end': 7}],
             'plant_margin_shape': [
                 {'start': 8, 'end': 28, 'margin_shape': 'corrugated'}]}
        )

    def test_margin_05(self):
        self.assertEqual(
            MATCHER.parse(shorten("""
                margins coarsely toothed or remotely sinuate-dentate
                to serrate,""")),
            {'subpart': [{'start': 0, 'end': 7, 'subpart': 'margin'}],
             'plant_margin_shape': [
                 {'start': 8, 'end': 24, 'margin_shape': 'toothed'},
                 {'start': 28, 'end': 52, 'margin_shape': 'sinuate-dentate'},
                 {'start': 56, 'end': 63, 'margin_shape': 'serrate'}]}
        )
