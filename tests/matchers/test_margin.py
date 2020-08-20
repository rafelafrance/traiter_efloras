"""Test the plant margin shape matcher."""

# pylint: disable=missing-function-docstring

import unittest

from traiter.pylib.util import shorten

from src.pylib.pipeline import trait_list


class TestMargin(unittest.TestCase):
    """Test the plant margin shape trait parser."""

    def test_margin_01(self):
        self.assertEqual(
            trait_list('margin shallowly undulate-crenate'),
            [{'subpart': 'margin', 'trait': 'subpart', 'start': 0, 'end': 6},
             {'margin_shape': 'undulate-crenate',
              'trait': 'plant_margin_shape',
              'start': 7,
              'end': 33}]
        )

    def test_margin_02(self):
        self.assertEqual(
            trait_list(
                'margins ciliate, apex acute to long-acuminate,'),
            [{'subpart': 'margin', 'trait': 'subpart', 'start': 0, 'end': 7},
             {'margin_shape': 'ciliate',
              'trait': 'plant_margin_shape',
              'start': 8,
              'end': 15},
             {'subpart': 'apex', 'trait': 'subpart', 'start': 17, 'end': 21},
             {'shape': 'acute', 'trait': 'plant_apex_shape', 'start': 22,
              'end': 27},
             {'shape': 'acuminate', 'trait': 'plant_apex_shape', 'start': 31,
              'end': 45}]
        )

    def test_margin_03(self):
        self.assertEqual(
            trait_list('reniform, undulate-margined'),
            [{'shape': 'reniform', 'trait': 'plant_shape', 'start': 0,
              'end': 8},
             {'margin_shape': 'undulate',
              'trait': 'plant_margin_shape',
              'start': 10,
              'end': 27}]
        )

    def test_margin_04(self):
        self.assertEqual(
            trait_list('margins thickened-corrugated'),
            [{'subpart': 'margin', 'trait': 'subpart', 'start': 0, 'end': 7},
             {'margin_shape': 'corrugated',
              'trait': 'plant_margin_shape',
              'start': 8,
              'end': 28}]
        )

    def test_margin_05(self):
        self.assertEqual(
            trait_list(shorten("""
                margins coarsely toothed or remotely sinuate-dentate
                to serrate,""")),
            [{'subpart': 'margin', 'trait': 'subpart', 'start': 0, 'end': 7},
             {'margin_shape': 'toothed',
              'trait': 'plant_margin_shape',
              'start': 8,
              'end': 24},
             {'margin_shape': 'sinuate-dentate',
              'trait': 'plant_margin_shape',
              'start': 28,
              'end': 52},
             {'margin_shape': 'serrate',
              'trait': 'plant_margin_shape',
              'start': 56,
              'end': 63}]
        )
