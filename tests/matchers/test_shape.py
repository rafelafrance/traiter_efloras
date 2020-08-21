"""Test the plant shape matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from src.pylib.ner import trait_list


class TestShape(unittest.TestCase):
    """Test the plant shape trait parser."""

    def test_shape_01(self):
        self.assertEqual(
            trait_list('leaf suborbiculate'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'shape': 'orbicular', 'trait': 'leaf_shape', 'start': 5,
              'end': 18}]
        )

    def test_shape_02(self):
        self.assertEqual(
            trait_list('leaf ovate-suborbicular'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'shape': 'ovate-orbicular', 'trait': 'leaf_shape', 'start': 5,
              'end': 23}]
        )

    def test_shape_03(self):
        self.assertEqual(
            trait_list(
                'petiolule narrowly oblanceolate,'),
            [{'part': 'petiole', 'trait': 'part', 'start': 0, 'end': 9},
             {'shape': 'oblanceolate', 'trait': 'petiole_shape', 'start': 10,
              'end': 31}]
        )

    def test_shape_04(self):
        self.assertEqual(
            trait_list(
                'Leaves ; blade ovate or orbiculate to '
                'suborbiculate or reniform,'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'part': 'leaf', 'trait': 'part', 'start': 9, 'end': 14},
             {'shape': 'ovate', 'trait': 'leaf_shape', 'start': 15, 'end': 20},
             {'shape': 'orbicular', 'trait': 'leaf_shape', 'start': 24,
              'end': 34},
             {'shape': 'orbicular', 'trait': 'leaf_shape', 'start': 38,
              'end': 51},
             {'shape': 'reniform', 'trait': 'leaf_shape', 'start': 55,
              'end': 63}]
        )

    def test_shape_05(self):
        self.assertEqual(
            trait_list(
                'Leaves: blade ovate or elongate-ovate to '
                'lanceolate-ovate or ovate-triangular, '),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'part': 'leaf', 'trait': 'part', 'start': 8, 'end': 13},
             {'shape': 'ovate', 'trait': 'leaf_shape', 'start': 14, 'end': 19},
             {'shape': 'elongate-ovate', 'trait': 'leaf_shape', 'start': 23,
              'end': 37},
             {'shape': 'lanceolate-ovate', 'trait': 'leaf_shape', 'start': 41,
              'end': 57},
             {'shape': 'ovate-triangular', 'trait': 'leaf_shape', 'start': 61,
              'end': 77}]
        )

    def test_shape_06(self):
        self.assertEqual(
            trait_list(
                'Leaves: blade broadly to shallowly triangular'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'part': 'leaf', 'trait': 'part', 'start': 8, 'end': 13},
             {'shape': 'triangular', 'trait': 'leaf_shape', 'start': 14,
              'end': 45}]
        )

    def test_shape_07(self):
        self.assertEqual(
            trait_list(
                '; blade abaxially, suborbiculate to '
                'broadly ovate, depressed-ovate, or reniform, '),
            [{'part': 'leaf', 'trait': 'part', 'start': 2, 'end': 7},
             {'shape': 'orbicular', 'trait': 'leaf_shape', 'start': 19,
              'end': 32},
             {'shape': 'ovate', 'trait': 'leaf_shape', 'start': 36, 'end': 49},
             {'shape': 'ovate', 'trait': 'leaf_shape', 'start': 51, 'end': 66},
             {'shape': 'reniform', 'trait': 'leaf_shape', 'start': 71,
              'end': 79}]
        )

    def test_shape_08(self):
        self.assertEqual(
            trait_list(
                'blade broadly ovate-cordate to triangular-cordate or '
                'reniform, shallowly to deeply palmately '),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'shape': 'ovate-cordate', 'trait': 'leaf_shape', 'start': 6,
              'end': 27},
             {'shape': 'triangular-cordate', 'trait': 'leaf_shape',
              'start': 31, 'end': 49},
             {'shape': 'reniform', 'trait': 'leaf_shape', 'start': 53,
              'end': 61}]
        )

    def test_shape_09(self):
        self.assertEqual(
            trait_list(
                'Leaf blades lobe apex rounded'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 11},
             {'subpart': 'lobe', 'trait': 'subpart', 'start': 12, 'end': 16},
             {'subpart': 'apex', 'trait': 'subpart', 'start': 17, 'end': 21},
             {'shape': 'orbicular', 'trait': 'leaf_apex_shape', 'start': 22,
              'end': 29}]
        )

    def test_shape_10(self):
        self.assertEqual(
            trait_list(
                'Leaf blades mostly orbiculate, deeply to shallowly lobed,'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 11},
             {'shape': 'orbicular', 'trait': 'leaf_shape', 'start': 12,
              'end': 29}]
        )

    def test_shape_11(self):
        self.assertEqual(
            trait_list(
                'Leaves: petiole blade pentagonal-angulate to '
                'reniform-angulate or shallowly 5-angulate'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'part': 'petiole', 'trait': 'part', 'start': 8, 'end': 21},
             {'shape': 'polygonal', 'trait': 'petiole_shape', 'start': 22,
              'end': 32},
             {'shape': 'reniform-polygonal',
              'trait': 'petiole_shape',
              'start': 45,
              'end': 62},
             {'shape': 'polygonal', 'trait': 'petiole_shape', 'start': 66,
              'end': 86}]
        )

    def test_shape_12(self):
        self.assertEqual(
            trait_list(
                'blade lanceolate to narrowly or broadly lanceolate '
                'or elliptic-lanceolate, '),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'shape': 'lanceolate', 'trait': 'leaf_shape', 'start': 6,
              'end': 16},
             {'shape': 'lanceolate', 'trait': 'leaf_shape', 'start': 32,
              'end': 50},
             {'shape': 'elliptic-lanceolate',
              'trait': 'leaf_shape',
              'start': 54,
              'end': 73}]
        )

    def test_shape_13(self):
        self.assertEqual(
            trait_list(
                'blade broadly ovate to rounded-cordate, subreniform, '
                'or deltate'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'shape': 'ovate', 'trait': 'leaf_shape', 'start': 6, 'end': 19},
             {'shape': 'orbicular-cordate', 'trait': 'leaf_shape', 'start': 23,
              'end': 38},
             {'shape': 'reniform', 'trait': 'leaf_shape', 'start': 40,
              'end': 51},
             {'shape': 'deltoid', 'trait': 'leaf_shape', 'start': 56,
              'end': 63}]
        )

    def test_shape_14(self):
        self.assertEqual(
            trait_list(
                'blade orbic-ulate to pentagonal,'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'shape': 'orbicular', 'trait': 'leaf_shape', 'start': 6,
              'end': 17},
             {'shape': 'polygonal', 'trait': 'leaf_shape', 'start': 21,
              'end': 31}]
        )

    def test_shape_15(self):
        self.assertEqual(
            trait_list('blade pen-tagonal'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'shape': 'polygonal', 'trait': 'leaf_shape', 'start': 6,
              'end': 17}]
        )

    def test_shape_16(self):
        """There is a soft hyphen in ellip­tic."""
        self.assertEqual(
            trait_list('Petals standard rhombic-ellip­tic to obovate,'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'shape': 'rhomboic-elliptic', 'trait': 'petal_shape',
              'start': 16, 'end': 33},
             {'shape': 'obovate', 'trait': 'petal_shape', 'start': 37,
              'end': 44}]
        )

    def test_shape_17(self):
        self.assertEqual(
            trait_list('<base truncate to cordate>'),
            [{'subpart': 'base', 'trait': 'subpart', 'start': 1, 'end': 5},
             {'shape': 'truncate', 'trait': 'plant_base_shape', 'start': 6,
              'end': 14},
             {'shape': 'cordate', 'trait': 'plant_base_shape', 'start': 18,
              'end': 25}]
        )

    def test_shape_18(self):
        self.assertEqual(
            trait_list('<base truncate to cordate>'),
            [{'subpart': 'base', 'trait': 'subpart', 'start': 1, 'end': 5},
             {'shape': 'truncate', 'trait': 'plant_base_shape', 'start': 6,
              'end': 14},
             {'shape': 'cordate', 'trait': 'plant_base_shape', 'start': 18,
              'end': 25}]
        )

    def test_shape_19(self):
        self.assertEqual(
            trait_list('Seeds globose-angular'),
            [{'part': 'seed', 'trait': 'part', 'start': 0, 'end': 5},
             {'shape': 'spheric', 'trait': 'seed_shape', 'start': 6,
              'end': 13}]
        )

    def test_shape_20(self):
        self.assertEqual(
            trait_list('bractlets narrowly to broadly ovate-triangular'),
            [{'part': 'bract', 'trait': 'part', 'start': 0, 'end': 9},
             {'shape': 'ovate-triangular', 'trait': 'bract_shape', 'start': 10,
              'end': 46}]
        )

    def test_shape_21(self):
        self.assertEqual(
            trait_list('Petals purple; bilobate;'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'purple', 'trait': 'petal_color', 'start': 7,
              'end': 13},
             {'start': 15, 'end': 23, 'low': 2, 'trait': 'petal_lobe_count'}]
        )
