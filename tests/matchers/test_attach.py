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
            {'part': [{'start': 0, 'end': 6, 'part': 'leaf'}],
             'petal_color': [{'color': 'yellow', 'start': 7, 'end': 25}]}
        )

    def test_attach_02(self):
        self.assertEqual(
            parse('perianth lobes elliptic, ca. 1 mm'),
            {'part': [{'start': 0, 'end': 8, 'part': 'perianth'}],
             'subpart': [{'subpart': 'lobe', 'start': 9, 'end': 14}],
             'perianth_lobe_shape': [
                 {'shape': 'elliptic', 'start': 15, 'end': 23}],
             'perianth_lobe_size': [{'start': 25, 'end': 33,
                                     'length_low': 1, 'length_units': 'mm'}]}
        )

    def test_attach_03(self):
        self.assertEqual(
            parse('fruits (1--)3-lobed,'),
            {'part': [{'start': 0, 'end': 6, 'part': 'fruit'}],
             'fruit_lobe_count': [{
                 'start': 7, 'end': 19, 'min': 1, 'low': 3}]}
        )

    def test_attach_04(self):
        self.assertEqual(
            parse('petals spreading, pink, unlobed,'),
            {'part': [{'start': 0, 'end': 6, 'part': 'petal'}],
             'petal_color': [{'color': 'pink', 'start': 18, 'end': 22}],
             'petal_lobe_count': [{'start': 24, 'end': 31, 'low': 0}]}
        )

    def test_attach_05(self):
        self.assertEqual(
            parse('Inflorescences 10+-flowered'),
            {'part': [{'start': 0, 'end': 14, 'part': 'inflorescence'}],
             'inflorescence_flower_count': [
                 {'start': 15, 'end': 27, 'low': 10, 'indefinite': True}]}
        )

    def test_attach_06(self):
        self.assertEqual(
            parse('blade [3–5-foliolate]'),
            {'part': [{'start': 0, 'end': 5, 'part': 'leaf'}],
             'leaf_count': [{'start': 6, 'end': 21, 'low': 3, 'high': 5}]}
        )

    def test_attach_07(self):
        self.assertEqual(
            parse('Racemes sessile, 2- or 3-flow­ered'),
            {'part': [{'part': 'inflorescence', 'start': 0, 'end': 7}],
             'inflorescence_flower_count': [
                 {'start': 17, 'end': 34, 'low': 2, 'high': 3}]}
        )

    def test_attach_08(self):
        self.assertEqual(
            parse('Legumes with a slender stipe 2-5 mm, 10-12 mm, ca. '
                  '4 mm high and ca. 3 mm wide, '),
            {'part': [{'part': 'legume', 'start': 0, 'end': 7}],
             'legume_stipe_size': [{'length_low': 2, 'length_high': 5,
                                    'length_units': 'mm',
                                    'start': 8, 'end': 35}],
             'legume_size': [{'length_low': 10, 'length_high': 12,
                              'length_units': 'mm',
                              'start': 37, 'end': 45},
                             {'height_low': 4, 'height_units': 'mm',
                              'start': 47, 'end': 60},
                             {'width_low': 3, 'width_units': 'mm', 'start': 65,
                              'end': 78}]}
        )
