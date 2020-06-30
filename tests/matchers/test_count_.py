"""Test plant count trait matcher."""

# pylint: disable=missing-function-docstring

import unittest

from traiter.util import shorten

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestCount(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_count_01(self):
        self.assertEqual(
            MATCHER.parse('Seeds [1–]3–12[–30]'),
            {'part': [{'start': 0, 'end': 5, 'part': 'seed'}],
             'seed_count': [{'start': 6, 'end': 19,
                             'min': 1, 'low': 3, 'high': 12, 'max': 30}]}
        )

    def test_count_02(self):
        """It parses a seed count."""
        self.assertEqual(
            MATCHER.parse('Seeds 3–12'),
            {'part': [{'start': 0, 'end': 5, 'part': 'seed'}],
             'seed_count': [{'start': 6, 'end': 10, 'low': 3, 'high': 12}]}
        )

    def test_count_03(self):
        self.assertEqual(
            MATCHER.parse('blade 5–10 × 4–9 cm'),
            {'part': [{'start': 0, 'end': 5, 'part': 'leaf'}],
             'leaf_size': [{'start': 6, 'end': 19,
                            'length_low': 5.0, 'length_high': 10.0,
                            'width_low': 4.0, 'width_high': 9.0,
                            'width_units': 'cm'}]}
        )

    def test_count_04(self):
        self.assertEqual(
            MATCHER.parse('petals 5, connate 1/2–2/3 length'),
            {'part': [{'start': 0, 'end': 6, 'part': 'petal'}],
             'petal_count': [{'start': 7, 'end': 8, 'low': 5}],
             'petal_shape': [{'shape': 'connate', 'start': 10, 'end': 17}]}
        )

    def test_count_05(self):
        self.assertEqual(
            MATCHER.parse('ovules mostly 120–200.'),
            {'part': [{'start': 0, 'end': 6, 'part': 'ovary'}],
             'ovary_count': [
                 {'start': 14, 'end': 21, 'low': 120, 'high': 200}]}
        )

    def test_count_06(self):
        self.assertEqual(
            MATCHER.parse('Staminate flowers (3–)5–10(–20)'),
            {'part': [
                {'start': 0, 'end': 17, 'sex': 'male', 'part': 'flower'}],
                'flower_count': [{'start': 18, 'end': 31,
                                  'min': 3, 'low': 5,
                                  'high': 10, 'max': 20,
                                  'sex': 'male'}]}
        )

    def test_count_07(self):
        self.assertEqual(
            MATCHER.parse('Ovaries (4 or)5,'),
            {'part': [{'start': 0, 'end': 7, 'part': 'ovary'}],
             'ovary_count': [{'start': 8, 'end': 15, 'min': 4, 'low': 5}]}
        )

    def test_count_08(self):
        self.assertEqual(
            MATCHER.parse('Seeds 5(or 6)'),
            {'part': [{'start': 0, 'end': 5, 'part': 'seed'}],
             'seed_count': [{'start': 6, 'end': 13, 'low': 5, 'max': 6}]}
        )

    def test_count_09(self):
        self.assertEqual(
            MATCHER.parse('Stamen [1–]3–12[–30]'),
            {'part': [{'start': 0, 'end': 6, 'part': 'stamen'}],
             'stamen_count': [{'start': 7, 'end': 20,
                               'min': 1, 'low': 3, 'high': 12, 'max': 30}]}
        )

    def test_count_10(self):
        self.assertEqual(
            MATCHER.parse('leaf (12-)23-34 × 45-56'),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 4}]}
        )

    def test_count_11(self):
        self.assertEqual(
            MATCHER.parse('stigma papillose on 1 side,'),
            {'part': [{'part': 'stigma', 'start': 0, 'end': 6}]}
        )

    def test_count_12(self):
        self.assertEqual(
            MATCHER.parse('Male flowers with 2-8(-20) stamens;'),
            {'part': [
                {'start': 0, 'end': 12, 'sex': 'male', 'part': 'flower'},
                {'sex': 'male', 'start': 27, 'end': 34, 'part': 'stamen'}],
                'stamen_count': [{'sex': 'male', 'start': 18, 'end': 26,
                                  'low': 2, 'high': 8, 'max': 20}]}
        )

    def test_count_13(self):
        self.assertEqual(
            MATCHER.parse('leaflets in 3 or 4 pairs,'),
            {'part': [{'start': 0, 'end': 8, 'part': 'leaflet'}],
             'leaflet_count': [
                 {'start': 12, 'end': 24, 'low': 3, 'high': 4,
                  'group': 'pairs'}]}
        )

    def test_count_14(self):
        self.assertEqual(
            MATCHER.parse('leaflets/lobes 11–23,'),
            {'part': [{'start': 0, 'end': 8, 'part': 'leaflet'}],
             'subpart': [{'subpart': 'lobe', 'start': 9, 'end': 14}],
             'leaflet_lobe_count': [
                 {'start': 15, 'end': 20, 'low': 11, 'high': 23}]}
        )

    def test_count_15(self):
        self.assertEqual(
            MATCHER.parse('leaflets in 3 or 4(or 5) pairs,'),
            {'part': [{'start': 0, 'end': 8, 'part': 'leaflet'}],
             'leaflet_count': [
                 {'start': 12, 'end': 30, 'low': 3, 'high': 4, 'max': 5,
                  'group': 'pairs'}]}
        )

    def test_count_16(self):
        self.assertEqual(
            MATCHER.parse('plants weigh up to 200 pounds'),
            {'part': [{'start': 0, 'end': 6, 'part': 'plant'}]}
        )

    def test_count_17(self):
        self.assertEqual(
            MATCHER.parse(shorten("""
                Pistillate flowers: hyaline bristle at apex of hypanthial 
                aculei 0.5–1 times as long as opaque base.""")),
            {'part': [
                {'start': 0, 'end': 18, 'sex': 'female', 'part': 'flower'}],
                'subpart': [
                    {'start': 39, 'end': 43, 'subpart': 'apex',
                     'sex': 'female'},
                    {'start': 58, 'end': 64, 'subpart': 'aculeus',
                     'sex': 'female'},
                    {'start': 95, 'end': 99, 'subpart': 'base',
                     'sex': 'female'}]}
        )

    def test_count_18(self):
        self.assertEqual(
            MATCHER.parse(shorten("""rarely 1- or 5-7-foliolate;""")),
            {'plant_leaf_count': [
                {'min': 1, 'low': 5, 'high': 7, 'start': 7, 'end': 26}]}
        )

    def test_count_19(self):
        self.assertEqual(
            MATCHER.parse(shorten(
                """Leaves imparipinnate, 5- or 7(or 9)-foliolate;""")),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 6}],
             'leaf_count': [
                 {'low': 5, 'high': 7, 'max': 9, 'start': 22, 'end': 45}]}
        )

    def test_count_20(self):
        self.assertEqual(
            MATCHER.parse('Seeds (1 or)2 or 3 per legume,'),
            {'part': [{'part': 'seed', 'start': 0, 'end': 5}],
             'seed_count': [
                 {'min': 1, 'low': 2, 'high': 3, 'start': 6, 'end': 18}]}
        )

    def test_count_21(self):
        self.assertEqual(
            MATCHER.parse('Racemes compact, 1- or 2- or 5-7-flowered'),
            {'part': [{'part': 'inflorescence', 'start': 0, 'end': 7}],
             'inflorescence_flower_count': [
                 {'min': 1, 'low': 2, 'high': 5, 'max': 7,
                  'start': 17, 'end': 41}]}
        )

    def test_count_22(self):
        self.assertEqual(
            MATCHER.parse('3(or 5-9)-foliolate;'),
            {'plant_leaf_count': [
                {'low': 3, 'high': 5, 'max': 9, 'start': 0, 'end': 19}]}
        )

    def test_count_23(self):
        self.assertEqual(
            MATCHER.parse('leaflets (2or)3- or 4(or 5)-paired'),
            {'part': [{'part': 'leaflet', 'start': 0, 'end': 8}],
             'leaflet_pair_count': [
                 {'min': 2, 'low': 3, 'high': 4, 'max': 5,
                  'start': 9, 'end': 34}]}
        )

    def test_count_24(self):
        self.assertEqual(
            MATCHER.parse('Leaves (19-)23- or 25-foliolate;'),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 6}],
             'leaf_count': [
                 {'min': 19, 'low': 23, 'high': 25, 'start': 7, 'end': 31}]}
        )
