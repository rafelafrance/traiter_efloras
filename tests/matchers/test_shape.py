"""Test the plant shape matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestShape(unittest.TestCase):
    """Test the plant shape trait parser."""

    def test_shape_01(self):
        self.assertEqual(
            MATCHER.parse('leaf suborbiculate'),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 4}],
             'leaf_shape': [{'shape': 'orbicular', 'start': 5, 'end': 18}]}
        )

    def test_shape_02(self):
        self.assertEqual(
            MATCHER.parse('leaf ovate-suborbicular'),
            {'part': [{'start': 0, 'end': 4, 'part': 'leaf'}],
             'leaf_shape': [
                 {'shape': 'ovate-orbicular', 'start': 5, 'end': 23}]}
        )

    def test_shape_03(self):
        self.assertEqual(
            MATCHER.parse(
                'petiolule narrowly oblanceolate,'),
            {'part': [{'start': 0, 'end': 9, 'part': 'petiole'}],
             'petiole_shape': [
                 {'shape': 'oblanceolate', 'start': 10, 'end': 31}]}
        )

    def test_shape_04(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves ; blade ovate or orbiculate to '
                'suborbiculate or reniform,'),
            {'part': [{'start': 0, 'end': 6, 'part': 'leaf'},
                      {'start': 9, 'end': 14, 'part': 'leaf'}],
             'leaf_shape': [{'shape': 'ovate', 'start': 15, 'end': 20},
                            {'shape': 'orbicular', 'start': 24, 'end': 34},
                            {'shape': 'orbicular', 'start': 38, 'end': 51},
                            {'shape': 'reniform', 'start': 55, 'end': 63}]}
        )

    def test_shape_05(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves: blade ovate or elongate-ovate to '
                'lanceolate-ovate or ovate-triangular, '),
            {'part': [{'start': 0, 'end': 6, 'part': 'leaf'},
                      {'start': 8, 'end': 13, 'part': 'leaf'}],
             'leaf_shape': [{'shape': 'ovate', 'start': 14, 'end': 19},
                            {'shape': 'elongate-ovate',
                             'start': 23, 'end': 37},
                            {'shape': 'lanceolate-ovate',
                             'start': 41, 'end': 57},
                            {'shape': 'ovate-triangular',
                             'start': 61, 'end': 77}]}
        )

    def test_shape_06(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves: blade broadly to shallowly triangular'),
            {'part': [{'start': 0, 'end': 6, 'part': 'leaf'},
                      {'start': 8, 'end': 13, 'part': 'leaf'}],
             'leaf_shape': [{'shape': 'triangular', 'start': 14, 'end': 45}]}
        )

    def test_shape_07(self):
        self.assertEqual(
            MATCHER.parse(
                '; blade abaxially, suborbiculate to '
                'broadly ovate, depressed-ovate, or reniform, '),
            {'part': [{'part': 'leaf', 'start': 2, 'end': 7}],
             'leaf_shape': [{'shape': 'orbicular', 'start': 19, 'end': 32},
                            {'shape': 'ovate', 'start': 36, 'end': 49},
                            {'shape': 'ovate', 'start': 51, 'end': 66},
                            {'shape': 'reniform', 'start': 71, 'end': 79}]}
        )

    def test_shape_08(self):
        self.assertEqual(
            MATCHER.parse(
                'blade broadly ovate-cordate to triangular-cordate or '
                'reniform, shallowly to deeply palmately '),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 5}],
             'leaf_shape': [{'shape': 'ovate-cordate', 'start': 6, 'end': 27},
                            {'shape': 'triangular-cordate', 'start': 31,
                             'end': 49},
                            {'shape': 'reniform', 'start': 53, 'end': 61}]}
        )

    def test_shape_09(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaf blades lobe apex rounded'),
            {'part': [{'start': 0, 'end': 11, 'part': 'leaf'}],
             'subpart': [{'subpart': 'lobe', 'start': 12, 'end': 16},
                         {'subpart': 'apex', 'start': 17, 'end': 21}],
             'leaf_apex_shape': [
                 {'shape': 'orbicular', 'start': 22, 'end': 29}]}
        )

    def test_shape_10(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaf blades mostly orbiculate, deeply to shallowly lobed,'),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 11}],
             'leaf_shape': [{'shape': 'orbicular', 'start': 12, 'end': 29}]}
        )

    def test_shape_11(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves: petiole blade pentagonal-angulate to '
                'reniform-angulate or shallowly 5-angulate'),
            {'part': [{'start': 0, 'end': 6, 'part': 'leaf'},
                      {'start': 8, 'end': 15, 'part': 'petiole'},
                      {'start': 16, 'end': 21, 'part': 'leaf'}],
             'leaf_shape': [{'shape': 'polygonal', 'start': 22, 'end': 41},
                            {'shape': 'reniform-polygonal', 'start': 45,
                             'end': 62},
                            {'shape': 'polygonal', 'start': 66, 'end': 86}]}
        )

    def test_shape_12(self):
        self.assertEqual(
            MATCHER.parse(
                'blade lanceolate to narrowly or broadly lanceolate '
                'or elliptic-lanceolate, '),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 5}],
             'leaf_shape': [{'shape': 'lanceolate', 'start': 6, 'end': 16},
                            {'shape': 'lanceolate', 'start': 32, 'end': 50},
                            {'shape': 'elliptic-lanceolate',
                             'start': 54, 'end': 73}]}
        )

    def test_shape_13(self):
        self.assertEqual(
            MATCHER.parse(
                'blade broadly ovate to rounded-cordate, subreniform, '
                'or deltate'),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 5}],
             'leaf_shape': [{'shape': 'ovate', 'start': 6, 'end': 19},
                            {'shape': 'orbicular-cordate',
                             'start': 23, 'end': 38},
                            {'shape': 'reniform', 'start': 40, 'end': 51},
                            {'shape': 'deltoid', 'start': 56, 'end': 63}]}
        )

    def test_shape_14(self):
        self.assertEqual(
            MATCHER.parse(
                'blade orbic-ulate to pentagonal,'),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 5}],
             'leaf_shape': [{'shape': 'orbicular',
                             'start': 6, 'end': 17},
                            {'shape': 'polygonal',
                             'start': 21, 'end': 31}]}
        )

    def test_shape_15(self):
        self.assertEqual(
            MATCHER.parse('blade pen-tagonal'),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 5}],
             'leaf_shape': [{'shape': 'polygonal', 'start': 6, 'end': 17}]}
        )

    def test_shape_16(self):
        """There is a soft hyphen in ellip­tic."""
        self.assertEqual(
            MATCHER.parse('Petals standard rhombic-ellip­tic to obovate,'),
            {'part': [{'part': 'petal', 'start': 0, 'end': 6}],
             'petal_shape': [
                 {'shape': 'rhomboic-elliptic', 'start': 16, 'end': 33},
                 {'shape': 'obovate', 'start': 37, 'end': 44}
             ]}
        )

    def test_shape_17(self):
        self.assertEqual(
            MATCHER.parse('<base truncate to cordate>'),
            {'subpart': [{'start': 1, 'end': 5, 'subpart': 'base'}],
             'plant_base_shape': [
                 {'shape': 'truncate', 'start': 6, 'end': 14},
                 {'shape': 'cordate', 'start': 18, 'end': 25}]}
        )
