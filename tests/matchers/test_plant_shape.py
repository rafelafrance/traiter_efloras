"""Test the plant shape matcher."""

import unittest

from efloras.matchers.plant_shape import PLANT_SHAPE
from efloras.pylib.util import DotDict as Trait


class TestPlantShape(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_plant_shape_01(self):
        """It finds a shape."""
        self.assertEqual(
            PLANT_SHAPE.parse('leaf suborbiculate'),
            [Trait(start=0, end=18, part='leaf', value=['orbicular'],
                   raw_value='suborbiculate')])

    def test_plant_shape_02(self):
        """It combines shapes."""
        self.assertEqual(
            PLANT_SHAPE.parse('leaf ovate-suborbicular'),
            [Trait(start=0, end=23, part='leaf', value=['ovate-orbicular'],
                   raw_value='ovate-suborbicular')])

    def test_plant_shape_03(self):
        """It gets a shape starter word."""
        self.assertEqual(
            PLANT_SHAPE.parse('petiolule 3–12 mm, narrowly oblanceolate,'),
            [Trait(start=0, end=40, part='petiolule', value=['oblanceolate'],
                   raw_value='narrowly oblanceolate')])

    def test_plant_shape_04(self):
        """It handles conjunctions."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'Leaves ; blade ovate or orbiculate to '
                'suborbiculate or reniform,'),
            [Trait(start=9, end=63, part='blade',
                   value=['ovate', 'orbicular', 'reniform'],
                   raw_value='ovate or orbiculate to '
                             'suborbiculate or reniform')])

    def test_plant_shape_05(self):
        """It handles prepositions."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'Leaves: blade ovate or elongate-ovate to '
                'lanceolate-ovate or ovate-triangular, '),
            [Trait(start=8, end=77, part='blade',
                   value=['ovate', 'elongate-ovate', 'lanceolate-ovate',
                          'ovate-triangular'],
                   raw_value='ovate or elongate-ovate to '
                             'lanceolate-ovate or ovate-triangular')])

    def test_plant_shape_06(self):
        """It handles complex shape starter phrases."""
        self.assertEqual(
            PLANT_SHAPE.parse('Leaves: blade broadly to shallowly triangular'),
            [Trait(start=8, end=45, part='blade', value=['triangular'],
                   raw_value='broadly to shallowly triangular')])

    def test_plant_shape_07(self):
        """It handles complex shape phrases."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                '; blade sometimes white-mottled abaxially, suborbiculate to '
                'broadly ovate, depressed-ovate, or reniform, '),
            [Trait(start=2, end=103, part='blade',
                   value=['orbicular', 'ovate', 'reniform'],
                   raw_value='suborbiculate to '
                             'broadly ovate, depressed-ovate, or reniform')])

    def test_plant_shape_08(self):
        """It does not pick up lobe notations."""
        self.assertEqual(
            PLANT_SHAPE.parse('blade deeply pedately 3-lobed'),
            [])

    def test_plant_shape_09(self):
        """It handles complex shape phrases."""
        self.maxDiff = None
        self.assertEqual(
            PLANT_SHAPE.parse(
                'blade <sometimes white-spotted at vein junctions>, '
                'broadly ovate-cordate to triangular-cordate or reniform, '
                'shallowly to deeply palmately '),
            [Trait(start=0, end=106, part='blade',
                   value=['ovate-cordate', 'triangular-cordate', 'reniform'],
                   raw_value='broadly ovate-cordate to triangular-cordate '
                             'or reniform')])

    def test_plant_shape_10(self):
        """It does not pick up a lobe notation in the middle of the text."""
        self.assertEqual(
            PLANT_SHAPE.parse('Leaf blades 2–7 cm wide, lobe apex rounded'),
            [Trait(start=25, end=42, part='lobe',
                   value=['orbicular'],
                   raw_value='rounded')])

    def test_plant_shape_11(self):
        """It allows a lobe notation after a shape notation."""
        self.assertEqual(
            PLANT_SHAPE.parse('Leaf blades mostly orbiculate, '
                              'deeply to shallowly lobed,'),
            [Trait(start=0, end=29, part='leaf blades', value=['orbicular'],
                   raw_value='mostly orbiculate')])

    def test_plant_shape_12(self):
        """It handles the n-angulate shape."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'Leaves: petiole 1–3(–4.5) cm; blade pentagonal-angulate to '
                'reniform-angulate or shallowly 5-angulate,'),
            [Trait(start=30, end=100, part='blade',
                   value=['polygonal', 'reniform-polygonal'],
                   raw_value='pentagonal-angulate to '
                             'reniform-angulate or shallowly 5-angulate')])

    def test_plant_shape_13(self):
        """It reduces complex shape notations."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'blade lanceolate to narrowly or broadly lanceolate '
                'or elliptic-lanceolate, '),
            [Trait(start=0, end=73, part='blade',
                   value=['lanceolate', 'elliptic-lanceolate'],
                   raw_value='lanceolate to narrowly or broadly lanceolate '
                             'or elliptic-lanceolate')])

    def test_plant_shape_14(self):
        """It reduces complex shape notations."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'blade broadly ovate to rounded-cordate, subreniform, '
                'or deltate'),
            [Trait(start=0, end=63, part='blade',
                   value=['ovate', 'orbicular-cordate', 'reniform', 'deltoid'
                          ],
                   raw_value='broadly ovate to rounded-cordate, subreniform, '
                             'or deltate')])

    def test_plant_shape_15(self):
        """It handles hyphenated words."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'blade orbic-ulate to pentagonal,'),
            [Trait(start=0, end=31, part='blade',
                   value=['orbicular', 'polygonal'],
                   raw_value='orbic-ulate to pentagonal')])

    def test_plant_shape_16(self):
        """It handles hyphenated words."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'blade pen-tagonal'),
            [Trait(start=0, end=17, part='blade',
                   value=['polygonal'], raw_value='pen-tagonal')])

    def test_plant_shape_17(self):
        """It gets the plant part location."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'Leaves usually in basal rosettes, sometimes cauline, '
                'usually alternate, sometimes opposite '),
            [Trait(start=0, end=51, part='leaves',
                   location=['basal', 'cauline'],
                   value=['rosettes'],
                   raw_value='basal rosettes, sometimes cauline')])

    def test_plant_shape_18(self):
        """It parses other shapes."""
        self.assertEqual(
            PLANT_SHAPE.parse('hypanthium cupulate'),
            [Trait(start=0, end=19, part='hypanthium',
                   value=['cup-shaped'], raw_value='cupulate')])

    def test_plant_shape_19(self):
        """It separates different shapes."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'hypanthium cupulate to shallowly campanulate;'),
            [Trait(start=0, end=44, part='hypanthium',
                   value=['cup-shaped', 'campanulate'],
                   raw_value='cupulate to shallowly campanulate')])

    def test_plant_shape_20(self):
        """It separates different shapes."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'hypanthium subcylindric to narrowly funnelform;'),
            [Trait(start=0, end=46, part='hypanthium',
                   value=['cylindrical', 'funnelform'],
                   raw_value='subcylindric to narrowly funnelform')])

    def test_plant_shape_21(self):
        """It separates different shapes."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'hypanthium narrowly campanulate to cylindric '
                '[obtriangular];'),
            [Trait(
                start=0, end=58, part='hypanthium',
                value=['campanulate', 'cylindric', 'obtriangular'],
                raw_value='narrowly campanulate to cylindric [obtriangular')])

    def test_plant_shape_22(self):
        """It gets sepal shapes."""
        self.assertEqual(
            PLANT_SHAPE.parse('sepals linear-subulate, 3–5 mm; '),
            [Trait(start=0, end=22, part='sepals',
                   value=['linear-subulate'],
                   raw_value='linear-subulate')])

    def test_plant_shape_23(self):
        """It picks up many shape notations."""
        self.assertEqual(
            PLANT_SHAPE.parse('sepals cylindrical, peltate, semiterete, '
                              'subcylindrical, subpeltate, subterete, '
                              'subulate, terete'),
            [Trait(start=0, end=96, part='sepals',
                   value=['cylindrical', 'peltate', 'semiterete',
                          'subpeltate', 'subterete',
                          'subulate', 'terete'],
                   raw_value='cylindrical, peltate, semiterete, '
                             'subcylindrical, subpeltate, subterete, '
                             'subulate, terete')])

    def test_plant_shape_24(self):
        """It does not pick up a lobe notation."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'blade unlobed or palmately, pedately, or pinnately lobed'),
            [])

    def test_plant_shape_25(self):
        """It gets an ovary shape."""
        self.assertEqual(
            PLANT_SHAPE.parse(
                'Pistillate flowers: ovary usually 1-locular, ovoid to '
                'elliptic-ovoid or subglobose'),
            [Trait(start=20, end=68, part='ovary',
                   value=['ovoid', 'elliptic-ovoid'],
                   raw_value='ovoid to elliptic-ovoid')])

    def test_plant_shape_26(self):
        """It gathers two locations."""
        self.assertEqual(
            PLANT_SHAPE.parse('Leaves in basal rosette and cauline'),
            [Trait(start=0, end=35, part='leaves',
                   location=['basal', 'cauline'],
                   value=['rosette'],
                   raw_value='basal rosette and cauline')])
