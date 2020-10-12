"""Test the plant margin shape matcher."""

# pylint: disable=missing-function-docstring

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from src.efloras_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestMargin(unittest.TestCase):
    """Test the plant margin shape trait parser."""

    def test_margin_01(self):
        self.assertEqual(
            NLP('margin shallowly undulate-crenate'),
            [{'subpart': 'margin', 'trait': 'subpart', 'start': 0, 'end': 6},
             {'margin_shape': 'undulate-crenate',
              'trait': 'margin_shape', 'part': 'plant', 'subpart': 'margin',
              'start': 7, 'end': 33}]
        )

    def test_margin_02(self):
        self.maxDiff = None
        self.assertEqual(
            NLP('margins ciliate, apex acute to long-acuminate,'),
            [{'subpart': 'margin', 'trait': 'subpart',
              'start': 0, 'end': 7},
             {'margin_shape': 'ciliate',
              'trait': 'margin_shape', 'subpart': 'margin', 'part': 'plant',
              'start': 8, 'end': 15},
             {'subpart': 'apex', 'trait': 'subpart', 'part': 'plant',
              'start': 17, 'end': 21},
             {'shape': 'acute', 'trait': 'shape', 'part': 'plant',
              'subpart': 'apex', 'start': 22, 'end': 27},
             {'shape': 'acuminate', 'trait': 'shape', 'part': 'plant',
              'subpart': 'apex', 'start': 31, 'end': 45}]
        )

    def test_margin_03(self):
        self.assertEqual(
            NLP('reniform, undulate-margined'),
            [{'shape': 'reniform', 'trait': 'shape', 'part': 'plant',
              'start': 0, 'end': 8},
             {'margin_shape': 'undulate',
              'trait': 'margin_shape', 'part': 'plant',
              'start': 10, 'end': 27}]
        )

    def test_margin_04(self):
        self.assertEqual(
            NLP('margins thickened-corrugated'),
            [{'subpart': 'margin', 'trait': 'subpart', 'start': 0, 'end': 7},
             {'margin_shape': 'corrugated',
              'trait': 'margin_shape', 'part': 'plant', 'subpart': 'margin',
              'start': 8, 'end': 28}]
        )

    def test_margin_05(self):
        self.assertEqual(
            NLP(shorten("""
                margins coarsely toothed or remotely sinuate-dentate
                to serrate,""")),
            [{'subpart': 'margin', 'trait': 'subpart', 'start': 0, 'end': 7},
             {'margin_shape': 'toothed',
              'trait': 'margin_shape', 'part': 'plant', 'subpart': 'margin',
              'start': 8, 'end': 24},
             {'margin_shape': 'sinuate-dentate',
              'trait': 'margin_shape', 'part': 'plant', 'subpart': 'margin',
              'start': 28, 'end': 52},
             {'margin_shape': 'serrate',
              'trait': 'margin_shape', 'part': 'plant', 'subpart': 'margin',
              'start': 56, 'end': 63}]
        )
