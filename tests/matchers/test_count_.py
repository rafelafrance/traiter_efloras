"""Test plant count trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from src.pylib.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestCount(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_count_01(self):
        self.assertEqual(
            NLP('Seeds [1–]3–12[–30]'),
            [{'part': 'seed', 'trait': 'part', 'start': 0, 'end': 5},
             {'min': 1, 'low': 3, 'high': 12, 'max': 30,
              'trait': 'seed_count', 'start': 6, 'end': 19}]
        )

    def test_count_02(self):
        """It parses a seed count."""
        self.assertEqual(
            NLP('Seeds 3–12'),
            [{'part': 'seed', 'trait': 'part', 'start': 0, 'end': 5},
             {'low': 3, 'high': 12, 'trait': 'seed_count', 'start': 6,
              'end': 10}]
        )

    def test_count_03(self):
        self.assertEqual(
            NLP('blade 5–10 × 4–9 cm'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 5, 'length_high': 10,
              'width_low': 4, 'width_high': 9, 'width_units': 'cm',
              'trait': 'leaf_size', 'start': 6, 'end': 19}]
        )

    def test_count_04(self):
        self.assertEqual(
            NLP('petals 5, connate 1/2–2/3 length'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'low': 5, 'trait': 'petal_count', 'start': 7, 'end': 8},
             {'shape': 'connate', 'trait': 'petal_shape', 'start': 10,
              'end': 17}]
        )

    def test_count_05(self):
        self.assertEqual(
            NLP('ovules mostly 120–200.'),
            [{'part': 'ovary', 'trait': 'part', 'start': 0, 'end': 6},
             {'low': 120, 'high': 200, 'trait': 'ovary_count', 'start': 14,
              'end': 21}]
        )

    def test_count_06(self):
        self.assertEqual(
            NLP('Staminate flowers (3–)5–10(–20)'),
            [{'sex': 'male', 'part': 'flower',
              'trait': 'part', 'start': 0, 'end': 17},
             {'min': 3, 'low': 5, 'high': 10, 'max': 20, 'sex': 'male',
              'trait': 'flower_count', 'start': 18, 'end': 31}]
        )

    def test_count_07(self):
        self.assertEqual(
            NLP('Ovaries (4 or)5,'),
            [{'part': 'ovary', 'trait': 'part', 'start': 0, 'end': 7},
             {'min': 4, 'low': 5,
              'trait': 'ovary_count', 'start': 8, 'end': 15}]
        )

    def test_count_08(self):
        self.assertEqual(
            NLP('Seeds 5(or 6)'),
            [{'part': 'seed', 'trait': 'part', 'start': 0, 'end': 5},
             {'low': 5, 'max': 6,
              'trait': 'seed_count', 'start': 6, 'end': 13}]
        )

    def test_count_09(self):
        self.assertEqual(
            NLP('Stamen [1–]3–12[–30]'),
            [{'part': 'stamen', 'trait': 'part', 'start': 0, 'end': 6},
             {'min': 1,
              'low': 3,
              'high': 12,
              'max': 30,
              'trait': 'stamen_count',
              'start': 7,
              'end': 20}]
        )

    def test_count_10(self):
        self.assertEqual(
            NLP('leaf (12-)23-34 × 45-56'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4}]
        )

    def test_count_11(self):
        self.assertEqual(
            NLP('stigma papillose on 1 side,'),
            [{'part': 'stigma', 'trait': 'part', 'start': 0, 'end': 6}]
        )

    def test_count_12(self):
        self.assertEqual(
            NLP('Male flowers with 2-8(-20) stamens;'),
            [{'sex': 'male', 'part': 'flower',
              'trait': 'part', 'start': 0, 'end': 12},
             {'low': 2, 'high': 8, 'max': 20, 'sex': 'male',
              'trait': 'stamen_count', 'start': 18, 'end': 26},
             {'part': 'stamen', 'sex': 'male',
              'trait': 'part', 'start': 27, 'end': 34}]
        )

    def test_count_13(self):
        self.assertEqual(
            NLP('leaflets in 3 or 4 pairs,'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'low': 3, 'high': 4, 'group': 'pairs',
              'trait': 'leaflet_count', 'start': 12, 'end': 24}]
        )

    def test_count_14(self):
        self.assertEqual(
            NLP('leaflets/lobes 11–23,'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'subpart': 'lobe', 'trait': 'subpart', 'start': 9, 'end': 14},
             {'low': 11, 'high': 23, 'trait': 'leaflet_lobe_count',
              'start': 15, 'end': 20}]
        )

    def test_count_15(self):
        self.assertEqual(
            NLP('leaflets in 3 or 4(or 5) pairs,'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'low': 3, 'high': 4, 'max': 5, 'group': 'pairs',
              'trait': 'leaflet_count', 'start': 12, 'end': 30}]
        )

    def test_count_16(self):
        self.assertEqual(
            NLP('plants weigh up to 200 pounds'),
            [{'part': 'plant', 'trait': 'part', 'start': 0, 'end': 6}]
        )

    def test_count_17(self):
        self.assertEqual(
            NLP(shorten("""
                Pistillate flowers: hyaline bristle at apex of hypanthial 
                aculei 0.5–1 times as long as opaque base.""")),
            [{'sex': 'female', 'part': 'flower',
              'trait': 'part', 'start': 0, 'end': 18},
             {'subpart': 'apex', 'sex': 'female',
              'trait': 'subpart', 'start': 39, 'end': 43},
             {'subpart': 'aculeus', 'sex': 'female',
              'trait': 'subpart', 'start': 58, 'end': 64},
             {'subpart': 'base', 'sex': 'female',
              'trait': 'subpart', 'start': 95, 'end': 99}]
        )

    def test_count_18(self):
        self.assertEqual(
            NLP(shorten("""rarely 1- or 5-7-foliolate;""")),
            [{'min': 1, 'low': 5, 'high': 7,
              'trait': 'plant_leaf_count', 'start': 7, 'end': 26}]
        )

    def test_count_19(self):
        self.assertEqual(
            NLP(shorten(
                """Leaves imparipinnate, 5- or 7(or 9)-foliolate;""")),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'low': 5, 'high': 7, 'max': 9, 'trait': 'leaf_count',
              'start': 22, 'end': 45}]
        )

    def test_count_20(self):
        self.assertEqual(
            NLP('Seeds (1 or)2 or 3 per legume,'),
            [{'part': 'seed', 'trait': 'part', 'start': 0, 'end': 5},
             {'min': 1, 'low': 2, 'high': 3, 'trait': 'seed_count', 'start': 6,
              'end': 18}]
        )

    def test_count_21(self):
        self.assertEqual(
            NLP('Racemes compact, 1- or 2- or 5-7-flowered'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 7},
             {'min': 1,
              'low': 2,
              'high': 5,
              'max': 7,
              'trait': 'inflorescence_flower_count',
              'start': 17,
              'end': 41}]
        )

    def test_count_22(self):
        self.assertEqual(
            NLP('3(or 5-9)-foliolate;'),
            [{'low': 3,
              'high': 5,
              'max': 9,
              'trait': 'plant_leaf_count',
              'start': 0,
              'end': 19}]
        )

    def test_count_23(self):
        self.assertEqual(
            NLP('leaflets (2or)3- or 4(or 5)-paired'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'min': 2,
              'low': 3,
              'high': 4,
              'max': 5,
              'trait': 'leaflet_pair_count',
              'start': 9,
              'end': 34}]
        )

    def test_count_24(self):
        self.assertEqual(
            NLP('Leaves (19-)23- or 25-foliolate;'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'min': 19,
              'low': 23,
              'high': 25,
              'trait': 'leaf_count',
              'start': 7,
              'end': 31}]
        )
