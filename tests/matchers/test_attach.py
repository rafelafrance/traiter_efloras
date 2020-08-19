"""Test attaching traits to plant parts."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten

from efloras.pylib.pipeline import parse


class TestAttach(unittest.TestCase):
    """Test attaching traits to plant parts."""

    def test_attach_01(self):
        self.assertEqual(
            parse(shorten("""leaves and yellow petals.""")),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'yellow', 'trait': 'petal_color',
              'start': 7, 'end': 25}]
        )

    def test_attach_02(self):
        self.assertEqual(
            parse('perianth lobes elliptic, ca. 1 mm'),
            [{'part': 'perianth', 'trait': 'part', 'start': 0, 'end': 8},
             {'subpart': 'lobe', 'trait': 'subpart', 'start': 9, 'end': 14},
             {'shape': 'elliptic', 'trait': 'perianth_lobe_shape', 'start': 15,
              'end': 23},
             {'length_low': 1, 'length_units': 'mm',
              'trait': 'perianth_lobe_size',
              'start': 25, 'end': 33}]
        )

    def test_attach_03(self):
        self.assertEqual(
            parse('fruits (1--)3-lobed,'),
            [{'part': 'fruit', 'trait': 'part', 'start': 0, 'end': 6},
             {'min': 1, 'low': 3, 'trait': 'fruit_lobe_count', 'start': 7,
              'end': 19}]
        )

    def test_attach_04(self):
        self.assertEqual(
            parse('petals spreading, pink, unlobed,'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'pink', 'trait': 'petal_color', 'start': 18, 'end': 22},
             {'start': 24, 'end': 31, 'low': 0, 'trait': 'petal_lobe_count'}]
        )

    def test_attach_05(self):
        self.assertEqual(
            parse('Inflorescences 10+-flowered'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 14},
             {'low': 10, 'indefinite': True,
              'trait': 'inflorescence_flower_count',
              'start': 15, 'end': 27}]
        )

    def test_attach_06(self):
        self.assertEqual(
            parse('blade [3–5-foliolate]'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'low': 3, 'high': 5, 'trait': 'leaf_count', 'start': 6,
              'end': 21}]
        )

    def test_attach_07(self):
        self.assertEqual(
            parse('Racemes sessile, 2- or 3-flowered'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 7},
             {'low': 2, 'high': 3,
              'trait': 'inflorescence_flower_count',
              'start': 17, 'end': 33}]
        )

    def test_attach_08(self):
        self.assertEqual(
            parse('Legumes with a slender stipe 2-5 mm, 10-12 mm, ca. '
                  '4 mm high and ca. 3 mm wide, '),
            [{'part': 'legume', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_low': 2, 'length_high': 5, 'length_units': 'mm',
              'trait': 'legume_stipe_size', 'start': 8, 'end': 35},
             {'length_low': 10, 'length_high': 12, 'length_units': 'mm',
              'trait': 'legume_size', 'start': 37, 'end': 45},
             {'height_low': 4, 'height_units': 'mm', 'trait': 'legume_size',
              'start': 47, 'end': 60},
             {'width_low': 3, 'width_units': 'mm', 'trait': 'legume_size',
              'start': 65, 'end': 78}]
        )
