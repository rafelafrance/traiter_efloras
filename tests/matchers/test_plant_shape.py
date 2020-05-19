"""Test the plant shape matcher."""

import unittest

from efloras.matchers.base import Base


class TestPlantShape(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_plant_shape_01(self):
        """It finds a shape."""
        self.assertEqual(
            Base('*_shape').parse('leaf suborbiculate'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 4, 'raw_value': 'leaf'}],
                'leaf_shape': [{'value': 'orbicular',
                                'start': 5, 'end': 18,
                                'raw_value': 'suborbiculate'}]}]
        )

    def test_plant_shape_02(self):
        """It combines shapes."""
        self.assertEqual(
            Base('*_shape').parse('leaf ovate-suborbicular'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 4, 'raw_value': 'leaf'}],
                'leaf_shape': [{'value': 'ovate-orbicular',
                                'start': 5, 'end': 23,
                                'raw_value': 'ovate-suborbicular'}]}]
        )

    def test_plant_shape_03(self):
        """It gets a shape starter word."""
        self.assertEqual(
            Base('*_shape').parse(
                'petiolule 3–12 mm, narrowly oblanceolate,'),
            [{'part': [{'value': 'petiole',
                        'start': 0, 'end': 9,
                        'raw_value': 'petiolule'}],
              'petiole_shape': [{'value': 'oblanceolate',
                                 'start': 19, 'end': 40,
                                 'raw_value': 'narrowly oblanceolate'}]}]
        )

    def test_plant_shape_04(self):
        """It handles multiple shapes."""
        self.assertEqual(
            Base('*_shape').parse(
                'Leaves ; blade ovate or orbiculate to '
                'suborbiculate or reniform,'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6,
                        'raw_value': 'Leaves'}]},
             {'part': [{'value': 'leaf', 'start': 9, 'end': 14,
                        'raw_value': 'blade'}],
              'leaf_shape': [{'value': 'ovate',
                              'start': 15, 'end': 20,
                              'raw_value': 'ovate'},
                             {'value': 'orbicular',
                              'start': 24, 'end': 34,
                              'raw_value': 'orbiculate'},
                             {'value': 'orbicular',
                              'start': 38, 'end': 51,
                              'raw_value': 'suborbiculate'},
                             {'value': 'reniform',
                              'start': 55, 'end': 63,
                              'raw_value': 'reniform'}]}]
        )

    def test_plant_shape_05(self):
        """It handles multiple shapes."""
        self.assertEqual(
            Base('*_shape').parse(
                'Leaves: blade ovate or elongate-ovate to '
                'lanceolate-ovate or ovate-triangular, '),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6,
                        'raw_value': 'Leaves'}]},
             {'part': [{'value': 'leaf', 'start': 8, 'end': 13,
                        'raw_value': 'blade'}],
              'leaf_shape': [{'value': 'ovate',
                              'start': 14, 'end': 19,
                              'raw_value': 'ovate'},
                             {'value': 'elongate-ovate',
                              'start': 23, 'end': 37,
                              'raw_value': 'elongate-ovate'},
                             {'value': 'lanceolate-ovate',
                              'start': 41, 'end': 57,
                              'raw_value': 'lanceolate-ovate'},
                             {'value': 'ovate-triangular',
                              'start': 61, 'end': 77,
                              'raw_value': 'ovate-triangular'}]}]
        )

    def test_plant_shape_06(self):
        """It handles complex shape starter phrases."""
        self.assertEqual(
            Base('*_shape').parse(
                'Leaves: blade broadly to shallowly triangular'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6,
                        'raw_value': 'Leaves'}]},
             {'part': [{'value': 'leaf', 'start': 8, 'end': 13,
                        'raw_value': 'blade'}],
              'leaf_shape': [{'value': 'triangular',
                              'start': 14, 'end': 45,
                              'raw_value':
                                  'broadly to shallowly triangular'}]}]
        )

    def test_plant_shape_07(self):
        """It handles complex shape phrases."""
        self.assertEqual(
            Base('leaf_shape').parse(
                '; blade sometimes white-mottled abaxially, suborbiculate to '
                'broadly ovate, depressed-ovate, or reniform, '),
            [{'part': [
                {'value': 'leaf', 'start': 2, 'end': 7, 'raw_value': 'blade'}],
                'leaf_shape': [{'value': 'orbicular',
                                'start': 43, 'end': 56,
                                'raw_value': 'suborbiculate'},
                               {'value': 'ovate',
                                'start': 60, 'end': 73,
                                'raw_value': 'broadly ovate'},
                               {'value': 'ovate',
                                'start': 75, 'end': 90,
                                'raw_value': 'depressed-ovate'},
                               {'value': 'reniform',
                                'start': 95, 'end': 103,
                                'raw_value': 'reniform'}]}]
        )

    def test_plant_shape_08(self):
        """It does not pick up lobe notations."""
        self.assertEqual(
            Base('*_shape').parse('blade deeply pedately 3-lobed'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 5,
                        'raw_value': 'blade'}]}]
        )

    def test_plant_shape_09(self):
        """It handles complex shape phrases."""
        self.maxDiff = None
        self.assertEqual(
            Base('*_shape').parse(
                'blade <sometimes white-spotted at vein junctions>, '
                'broadly ovate-cordate to triangular-cordate or reniform, '
                'shallowly to deeply palmately '),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5, 'raw_value': 'blade'}],
                'leaf_shape': [{'value': 'ovate-cordate',
                                'start': 51, 'end': 72,
                                'raw_value': 'broadly ovate-cordate'},
                               {'value': 'triangular-cordate',
                                'start': 76, 'end': 94,
                                'raw_value': 'triangular-cordate'},
                               {'value': 'reniform',
                                'start': 98, 'end': 106,
                                'raw_value': 'reniform'}]}]
        )

    def test_plant_shape_10(self):
        """It does not pick up a lobe notation in the middle of the text."""
        self.assertEqual(
            Base('*_shape').parse(
                'Leaf blades 2–7 cm wide, lobe apex rounded'),
            [{'part': [{'value': 'leaf',
                        'start': 0, 'end': 11,
                        'raw_value': 'Leaf blades'}]},
             {'part': [{'value': 'lobes', 'start': 25, 'end': 29,
                        'raw_value': 'lobe'}]}]

        )

    def test_plant_shape_11(self):
        """It allows a lobe notation after a shape notation."""
        self.assertEqual(
            Base('*_shape').parse(
                'Leaf blades mostly orbiculate, deeply to shallowly lobed,'),
            [{'part': [{'value': 'leaf',
                        'start': 0, 'end': 11,
                        'raw_value': 'Leaf blades'}],
              'leaf_shape': [{'value': 'orbicular',
                              'start': 12, 'end': 29,
                              'raw_value': 'mostly orbiculate'}]}]
        )

    def test_plant_shape_12(self):
        """It handles the n-angulate shape."""
        self.assertEqual(
            Base('*_shape').parse(
                'Leaves: petiole 1–3(–4.5) cm; blade pentagonal-angulate to '
                'reniform-angulate or shallowly 5-angulate,'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6,
                        'raw_value': 'Leaves'}]},
             {'part': [{'value': 'petiole',
                        'start': 8, 'end': 15,
                        'raw_value': 'petiole'}]},
             {'part': [{'value': 'leaf', 'start': 30, 'end': 35,
                        'raw_value': 'blade'}],
              'leaf_shape': [{'value': 'polygonal',
                              'start': 36, 'end': 55,
                              'raw_value': 'pentagonal-angulate'},
                             {'value': 'reniform-polygonal',
                              'start': 59, 'end': 76,
                              'raw_value': 'reniform-angulate'},
                             {'value': 'polygonal',
                              'start': 80, 'end': 100,
                              'raw_value': 'shallowly 5-angulate'}]}]
        )

    def test_plant_shape_13(self):
        """It more complex shape notations."""
        self.assertEqual(
            Base('*_shape').parse(
                'blade lanceolate to narrowly or broadly lanceolate '
                'or elliptic-lanceolate, '),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5, 'raw_value': 'blade'}],
                'leaf_shape': [{'value': 'lanceolate',
                                'start': 6, 'end': 16,
                                'raw_value': 'lanceolate'},
                               {'value': 'lanceolate',
                                'start': 32, 'end': 50,
                                'raw_value': 'broadly lanceolate'},
                               {'value': 'elliptic-lanceolate',
                                'start': 54, 'end': 73,
                                'raw_value': 'elliptic-lanceolate'}]}]
        )

    def test_plant_shape_14(self):
        """It more complex shape notations."""
        self.assertEqual(
            Base('*_shape').parse(
                'blade broadly ovate to rounded-cordate, subreniform, '
                'or deltate'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5, 'raw_value': 'blade'}],
                'leaf_shape': [{'value': 'ovate',
                                'start': 6, 'end': 19,
                                'raw_value': 'broadly ovate'},
                               {'value': 'orbicular-cordate',
                                'start': 23, 'end': 38,
                                'raw_value': 'rounded-cordate'},
                               {'value': 'reniform',
                                'start': 40, 'end': 51,
                                'raw_value': 'subreniform'},
                               {'value': 'deltoid',
                                'start': 56, 'end': 63,
                                'raw_value': 'deltate'}]}]
        )

    def test_plant_shape_15(self):
        """It handles hyphenated words."""
        self.assertEqual(
            Base('*_shape').parse(
                'blade orbic-ulate to pentagonal,'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5, 'raw_value': 'blade'}],
                'leaf_shape': [{'value': 'orbicular',
                                'start': 6, 'end': 17,
                                'raw_value': 'orbic-ulate'},
                               {'value': 'polygonal',
                                'start': 21, 'end': 31,
                                'raw_value': 'pentagonal'}]}]
        )

    def test_plant_shape_16(self):
        """It handles hyphenated words."""
        self.assertEqual(
            Base('*_shape').parse('blade pen-tagonal'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5, 'raw_value': 'blade'}],
                'leaf_shape': [{'value': 'polygonal',
                                'start': 6, 'end': 17,
                                'raw_value': 'pen-tagonal'}]}]
        )

    def test_plant_shape_17(self):
        """It gets the plant part location."""
        self.assertEqual(
            Base('*_shape').parse(
                'Leaves usually in basal rosettes, sometimes cauline, '
                'usually alternate, sometimes opposite '),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6,
                        'raw_value': 'Leaves'}],
              'leaf_location': [{'value': 'basal',
                                 'start': 18, 'end': 23,
                                 'raw_value': 'basal'},
                                {'value': 'cauline',
                                 'start': 44, 'end': 51,
                                 'raw_value': 'cauline'}],
              'leaf_shape': [{'value': 'rosettes',
                              'start': 24, 'end': 32,
                              'raw_value': 'rosettes'}]}]
        )

    def test_plant_shape_18(self):
        """It parses other shapes."""
        self.assertEqual(
            Base('*_shape').parse('hypanthium cupulate'),
            [{'part': [{'value': 'hypanthium',
                        'start': 0, 'end': 10,
                        'raw_value': 'hypanthium'}],
              'hypanthium_shape': [{'value': 'cup-shaped',
                                    'start': 11, 'end': 19,
                                    'raw_value': 'cupulate'}]}]
        )

    def test_plant_shape_19(self):
        """More multiple shape parsing."""
        self.assertEqual(
            Base('*_shape').parse(
                'hypanthium cupulate to shallowly campanulate;'),
            [{'part': [{'value': 'hypanthium',
                        'start': 0, 'end': 10,
                        'raw_value': 'hypanthium'}],
              'hypanthium_shape': [{'value': 'cup-shaped',
                                    'start': 11, 'end': 19,
                                    'raw_value': 'cupulate'},
                                   {'value': 'campanulate',
                                    'start': 23, 'end': 44,
                                    'raw_value': 'shallowly campanulate'}]}]
        )

    def test_plant_shape_20(self):
        """It separates different shapes."""
        self.assertEqual(
            Base('*_shape').parse(
                'hypanthium subcylindric to narrowly funnelform;'),
            [{'part': [{'value': 'hypanthium',
                        'start': 0, 'end': 10,
                        'raw_value': 'hypanthium'}],
              'hypanthium_shape': [{'value': 'cylindrical',
                                    'start': 11, 'end': 23,
                                    'raw_value': 'subcylindric'},
                                   {'value': 'funnelform',
                                    'start': 27, 'end': 46,
                                    'raw_value': 'narrowly funnelform'}]}]
        )

    def test_plant_shape_21(self):
        """It separates different shapes."""
        self.assertEqual(
            Base('*_shape').parse(
                'hypanthium narrowly campanulate to cylindric '
                '[obtriangular];'),
            [{'part': [{'value': 'hypanthium',
                        'start': 0, 'end': 10,
                        'raw_value': 'hypanthium'}],
              'hypanthium_shape': [{'value': 'campanulate',
                                    'start': 11, 'end': 31,
                                    'raw_value': 'narrowly campanulate'},
                                   {'value': 'cylindric',
                                    'start': 35, 'end': 44,
                                    'raw_value': 'cylindric'},
                                   {'value': 'obtriangular',
                                    'start': 46, 'end': 58,
                                    'raw_value': 'obtriangular'}]}]
        )

    def test_plant_shape_22(self):
        """It gets sepal shapes."""
        self.assertEqual(
            Base('sepal_shape').parse('sepals linear-subulate, 3–5 mm; '),
            [{'part': [{'value': 'sepal', 'start': 0, 'end': 6,
                        'raw_value': 'sepals'}],
              'sepal_shape': [{'value': 'linear-subulate',
                               'start': 7, 'end': 22,
                               'raw_value': 'linear-subulate'}]}]
        )

    def test_plant_shape_23(self):
        """It picks up many shape notations."""
        self.assertEqual(
            Base('*_shape').parse(
                'sepals cylindrical, peltate, semiterete, subcylindrical, '
                'subpeltate, subterete, subulate, terete'),
            [{'part': [{'value': 'sepal', 'start': 0, 'end': 6,
                        'raw_value': 'sepals'}],
              'sepal_shape': [{'value': 'cylindrical',
                               'start': 7, 'end': 18,
                               'raw_value': 'cylindrical'},
                              {'value': 'peltate',
                               'start': 20, 'end': 27,
                               'raw_value': 'peltate'},
                              {'value': 'semiterete',
                               'start': 29, 'end': 39,
                               'raw_value': 'semiterete'},
                              {'value': 'cylindrical',
                               'start': 41, 'end': 55,
                               'raw_value': 'subcylindrical'},
                              {'value': 'subpeltate',
                               'start': 57, 'end': 67,
                               'raw_value': 'subpeltate'},
                              {'value': 'subterete',
                               'start': 69, 'end': 78,
                               'raw_value': 'subterete'},
                              {'value': 'subulate',
                               'start': 80, 'end': 88,
                               'raw_value': 'subulate'},
                              {'value': 'terete',
                               'start': 90, 'end': 96,
                               'raw_value': 'terete'}]}]
        )

    def test_plant_shape_24(self):
        """It does not pick up a lobe notation."""
        self.assertEqual(
            Base('*_shape').parse(
                'blade unlobed or palmately, pedately, or pinnately lobed'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 5,
                        'raw_value': 'blade'}]},
             {'part': [{'value': 'lobes', 'start': 6, 'end': 13,
                        'raw_value': 'unlobed'}]}]
        )

    def test_plant_shape_25(self):
        """It does not get an ovary shape."""
        self.assertEqual(
            Base('*_shape').parse(
                'Pistillate flowers: ovary usually 1-locular, ovoid to '
                'elliptic-ovoid or subglobose'),
            [{'part': [{'value': 'flower',
                        'start': 0, 'end': 18,
                        'raw_value': 'Pistillate flowers',
                        'sex': 'pistillate'}]},
             {'part': [{'value': 'ovary', 'start': 20, 'end': 25,
                        'raw_value': 'ovary'}]}]
        )

    def test_plant_shape_26(self):
        """It gathers two locations."""
        self.assertEqual(
            Base('*_shape').parse('Leaves in basal rosette and cauline'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6,
                        'raw_value': 'Leaves'}],
              'leaf_location': [{'value': 'basal',
                                 'start': 10, 'end': 15,
                                 'raw_value': 'basal'},
                                {'value': 'cauline',
                                 'start': 28, 'end': 35,
                                 'raw_value': 'cauline'}],
              'leaf_shape': [{'value': 'rosette',
                              'start': 16, 'end': 23,
                              'raw_value': 'rosette'}]}]
        )
