"""Test the plant shape matcher."""

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestPlantShape(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_plant_shape_01(self):
        self.assertEqual(
            MATCHER.parse('leaf suborbiculate'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 4}],
                'leaf_shape': [{'value': 'orbicular', 'start': 5, 'end': 18}]}]
        )

    def test_plant_shape_02(self):
        self.assertEqual(
            MATCHER.parse('leaf ovate-suborbicular'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 4}],
                'leaf_shape': [{'value': 'ovate-orbicular',
                                'start': 5, 'end': 23}]}]
        )

    def test_plant_shape_03(self):
        self.assertEqual(
            MATCHER.parse(
                'petiolule narrowly oblanceolate,'),
            [{'part': [{'value': 'petiole', 'start': 0, 'end': 9}],
              'petiole_shape': [
                  {'value': 'oblanceolate', 'start': 10, 'end': 31}]}]
        )

    def test_plant_shape_04(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves ; blade ovate or orbiculate to '
                'suborbiculate or reniform,'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6}]},
             {'part': [{'value': 'leaf', 'start': 9, 'end': 14}],
              'leaf_shape': [{'value': 'ovate', 'start': 15, 'end': 20},
                             {'value': 'orbicular', 'start': 24, 'end': 34},
                             {'value': 'orbicular', 'start': 38, 'end': 51},
                             {'value': 'reniform', 'start': 55, 'end': 63}]}]
        )

    def test_plant_shape_05(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves: blade ovate or elongate-ovate to '
                'lanceolate-ovate or ovate-triangular, '),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6}]},
             {'part': [{'value': 'leaf', 'start': 8, 'end': 13}],
              'leaf_shape': [{'value': 'ovate', 'start': 14, 'end': 19},
                             {'value': 'elongate-ovate',
                              'start': 23, 'end': 37},
                             {'value': 'lanceolate-ovate',
                              'start': 41, 'end': 57},
                             {'value': 'ovate-triangular',
                              'start': 61, 'end': 77}]}]
        )

    def test_plant_shape_06(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves: blade broadly to shallowly triangular'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6}]},
             {'part': [{'value': 'leaf', 'start': 8, 'end': 13}],
              'leaf_shape': [{'value': 'triangular', 'start': 14, 'end': 45}]}]
        )

    def test_plant_shape_07(self):
        self.assertEqual(
            MATCHER.parse(
                '; blade abaxially, suborbiculate to '
                'broadly ovate, depressed-ovate, or reniform, '),
            [{'part': [{'value': 'leaf', 'start': 2, 'end': 7}],
              'leaf_shape': [{'value': 'orbicular', 'start': 19, 'end': 32},
                             {'value': 'ovate', 'start': 36, 'end': 49},
                             {'value': 'ovate', 'start': 51, 'end': 66},
                             {'value': 'reniform', 'start': 71, 'end': 79}]}]
        )

    def test_plant_shape_08(self):
        self.maxDiff = None
        self.assertEqual(
            MATCHER.parse(
                'blade broadly ovate-cordate to triangular-cordate or '
                'reniform, shallowly to deeply palmately '),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 5}],
              'leaf_shape': [{'value': 'ovate-cordate', 'start': 6, 'end': 27},
                             {'value': 'triangular-cordate', 'start': 31,
                              'end': 49},
                             {'value': 'reniform', 'start': 53, 'end': 61}]}]
        )

    def test_plant_shape_09(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaf blades lobe apex rounded'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 11}],
              'leaf_shape': [{'value': 'orbicular', 'start': 22, 'end': 29}]}]
        )

    def test_plant_shape_10(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaf blades mostly orbiculate, deeply to shallowly lobed,'),
            [{'part': [{'value': 'leaf',
                        'start': 0, 'end': 11}],
              'leaf_shape': [{'value': 'orbicular',
                              'start': 12, 'end': 29}]}]
        )

    def test_plant_shape_11(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves: petiole blade pentagonal-angulate to '
                'reniform-angulate or shallowly 5-angulate'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6}]},
             {'part': [{'value': 'petiole', 'start': 8, 'end': 15}]},
             {'part': [{'value': 'leaf', 'start': 16, 'end': 21}],
              'leaf_shape': [{'value': 'polygonal', 'start': 22, 'end': 41},
                             {'value': 'reniform-polygonal',
                              'start': 45, 'end': 62},
                             {'value': 'polygonal', 'start': 66, 'end': 86}]}]
        )

    def test_plant_shape_12(self):
        self.assertEqual(
            MATCHER.parse(
                'blade lanceolate to narrowly or broadly lanceolate '
                'or elliptic-lanceolate, '),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5}],
                'leaf_shape': [{'value': 'lanceolate',
                                'start': 6, 'end': 16},
                               {'value': 'lanceolate',
                                'start': 32, 'end': 50},
                               {'value': 'elliptic-lanceolate',
                                'start': 54, 'end': 73}]}]
        )

    def test_plant_shape_13(self):
        self.assertEqual(
            MATCHER.parse(
                'blade broadly ovate to rounded-cordate, subreniform, '
                'or deltate'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5}],
                'leaf_shape': [{'value': 'ovate', 'start': 6, 'end': 19},
                               {'value': 'orbicular-cordate',
                                'start': 23, 'end': 38},
                               {'value': 'reniform',
                                'start': 40, 'end': 51},
                               {'value': 'deltoid',
                                'start': 56, 'end': 63}]}]
        )

    def test_plant_shape_14(self):
        self.assertEqual(
            MATCHER.parse(
                'blade orbic-ulate to pentagonal,'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5}],
                'leaf_shape': [{'value': 'orbicular',
                                'start': 6, 'end': 17},
                               {'value': 'polygonal',
                                'start': 21, 'end': 31}]}]
        )

    def test_plant_shape_15(self):
        self.assertEqual(
            MATCHER.parse('blade pen-tagonal'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5}],
                'leaf_shape': [{'value': 'polygonal',
                                'start': 6, 'end': 17}]}]
        )
