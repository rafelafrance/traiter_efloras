"""Test plant size trait matcher."""

import unittest

from efloras.matchers.plant_size import PLANT_SIZE
from efloras.pylib.util import DotDict as Trait


class TestPlantSize(unittest.TestCase):
    """Test plant size trait parsers."""

    def test_plant_size_01(self):
        """It parses a cross measurement."""
        self.assertEqual(
            PLANT_SIZE.parse('Leaf (12-)23-34 × 45-56 cm'),
            [Trait(start=0, end=26, part='leaf', units='cm',
                   min_length=120, low_length=230, high_length=340,
                   low_width=450, high_width=560)])

    def test_plant_size_02(self):
        """Units are required."""
        self.assertEqual(
            PLANT_SIZE.parse('(12-)23-34 × 45-56'),
            [])

    def test_plant_size_03(self):
        """It parses a range simple measurement."""
        self.assertEqual(
            PLANT_SIZE.parse('blade 1.5–5(–7) cm'),
            [Trait(part='blade', start=0, end=18, units='cm',
                   low_length=15, high_length=50, max_length=70)])

    def test_plant_size_04(self):
        """It does not allow trailing dashes."""
        self.assertEqual(
            PLANT_SIZE.parse('shallowly to deeply 5–7-lobed'),
            [])

    def test_plant_size_05(self):
        """It get a dimension."""
        self.assertEqual(
            PLANT_SIZE.parse('leaf 4–10 cm wide'),
            [Trait(start=0, end=17, units='cm',
                   low_length=40, high_length=100,
                   part='leaf', dimension='wide')])

    def test_plant_size_06(self):
        """It does not interpret fractions as a range."""
        self.assertEqual(
            PLANT_SIZE.parse('sinuses 1/5–1/4 to base'),
            [])

    def test_plant_size_07(self):
        """It allows a simple range."""
        self.assertEqual(
            PLANT_SIZE.parse('petiolules 2–5 mm'),
            [Trait(part='petiolules', start=0, end=17, units='mm',
                   low_length=2, high_length=5)])

    def test_plant_size_08(self):
        """It picks up multiple measurements."""
        self.assertEqual(
            PLANT_SIZE.parse(
                'petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm.'),
            [Trait(part='petiolules', start=0, end=17, units='mm',
                   low_length=2.0, high_length=5.0),
             Trait(part='petioles', start=37, end=54, units='mm',
                   low_length=16.0, high_length=28.0)])

    def test_plant_size_09(self):
        """It allows a simple range."""
        self.assertEqual(
            PLANT_SIZE.parse('Leaves: petiole 2–15 cm;'),
            [Trait(part='petiole', start=8, end=23, units='cm',
                   low_length=20, high_length=150)])

    def test_plant_size_10(self):
        """It allows alternate opening and closing brackets."""
        self.assertEqual(
            PLANT_SIZE.parse(
                'oblong [suborbiculate], petiole [5–]7–25[–32] mm, glabrous,'),
            [Trait(start=24, end=48, part='petiole', units='mm',
                   low_length=7, high_length=25,
                   min_length=5, max_length=32)])

    def test_plant_size_11(self):
        """It handles different units for width and length."""
        self.assertEqual(
            PLANT_SIZE.parse('leaf 2–4 cm × 2–10 mm'),
            [Trait(start=0, end=21, part='leaf', units=['cm', 'mm'],
                   low_length=20.0, high_length=40.0,
                   low_width=2.0, high_width=10.0)])

    def test_plant_size_12(self):
        """It does not pick up a lobe measurement."""
        self.assertEqual(
            PLANT_SIZE.parse('deeply to shallowly lobed, 4–5(–7) cm wide,'),
            [])

    def test_plant_size_13(self):
        """It handles a range after a lobe notation."""
        self.assertEqual(
            PLANT_SIZE.parse('Leaves 3-foliolate, lateral pair of leaflets '
                             'deeply lobed, petiolules 2–5 mm,'),
            [Trait(start=59, end=76, part='petiolules',
                   low_length=2, high_length=5, units='mm')])

    def test_plant_size_14(self):
        """It gets a location with the size."""
        self.maxDiff = None
        self.assertEqual(
            PLANT_SIZE.parse('terminal leaflet 3–5 cm, blade '
                             'narrowly lanceolate, petiolule 3–12 mm,'),
            [
                Trait(start=0, end=23, location='terminal', part='leaflet',
                      units='cm', low_length=30.0, high_length=50.0),
                Trait(start=52, end=69, part='petiolule',
                      units='mm', low_length=3.0, high_length=12.0),
            ])

    def test_plant_size_15(self):
        """It does not pick up lobe sizes."""
        self.assertEqual(
            PLANT_SIZE.parse('shallowly 3–5(–7)-lobed, '
                             '5–25 × (8–)10–25(–30) cm,'),
            [])

    def test_plant_size_16(self):
        """It does not pick up lobe sizes."""
        self.assertEqual(
            PLANT_SIZE.parse('(3–)5-lobed, 6–20(–30) × 6–25 cm,'),
            [])

    def test_plant_size_17(self):
        """It does not pick up lobe sizes."""
        self.assertEqual(
            PLANT_SIZE.parse('blade deeply pedately 3-lobed, 2–6 cm wide'),
            [Trait(start=0, end=42, part='blade', dimension='wide',
                   units='cm', low_length=20, high_length=60)])

    def test_plant_size_18(self):
        """It allows an 'up to' type of size notation."""
        self.assertEqual(
            PLANT_SIZE.parse('petiole to 11 cm;'),
            [Trait(start=0, end=16, part='petiole', units='cm',
                   high_length=110)])

    def test_plant_size_19(self):
        """It allows both length and width ranges."""
        self.assertEqual(
            PLANT_SIZE.parse('blade ovate to depressed-ovate or flabellate, '
                             '5-17(-20) × (3-)6-16 mm'),
            [Trait(start=0, end=69, part='blade', units='mm',
                   low_length=5.0, high_length=17.0, max_length=20.0,
                   min_width=3.0, low_width=6.0, high_width=16.0)])

    def test_plant_size_20(self):
        """It allows both length and width ranges."""
        self.assertEqual(
            PLANT_SIZE.parse('blade ovate to depressed-ovate, round, '
                             'or flabellate, 2.5-15 × 2-10(-20) mm,'),
            [Trait(start=0, end=75, part='blade', units='mm',
                   low_length=2.5, high_length=15.0,
                   low_width=2.0, high_width=10.0, max_width=20.0)])

    def test_plant_size_21(self):
        """It allows both length and width ranges."""
        self.assertEqual(
            PLANT_SIZE.parse('blade broadly cordate to broadly ovate, ± as '
                             'long as wide, 1.2-6.5(-8.5) × 1.4-7(-8.2) cm'),
            [Trait(start=0, end=89, part='blade', units='cm',
                   low_length=12.0, high_length=65.0, max_length=85.0,
                   low_width=14.0, high_width=70.0, max_width=82.0)])

    def test_plant_size_22(self):
        """It handles a 'to' in the range with both length & width ranges."""
        self.assertEqual(
            PLANT_SIZE.parse('blade pentagonal-angulate to reniform-angulate '
                             'or shallowly 5-angulate, sinuses 1/4–1/3 to '
                             'base, (3–)4–7 × 5–9 cm'),
            [Trait(start=0, end=113, part='blade', units='cm',
                   min_length=30, low_length=40, high_length=70,
                   low_width=50, high_width=90)])

    def test_plant_size_23(self):
        """It handles sexual dimorphism in size notations."""
        self.assertEqual(
            PLANT_SIZE.parse('petals (1–)3–10(–12) mm (pistillate) '
                             'or 5–8(–10) mm (staminate)'),
            [Trait(start=0, end=35,
                   part='petals', sex='pistillate', units='mm',
                   min_length=1.0, low_length=3.0, high_length=10.0,
                   max_length=12.0),
             Trait(start=0, end=62,
                   part='petals', sex='staminate', units='mm',
                   low_length=5.0, high_length=8.0, max_length=10.0)])

    def test_plant_size_24(self):
        """It handles a cross notaion for blade sizes."""
        self.assertEqual(
            PLANT_SIZE.parse('blade hastate to 5-angular, palmately '
                             '3–5-lobed, 3–8(–15) × 2–6(–8) cm,'),
            [Trait(start=0, end=70, part='blade', units='cm',
                   low_length=30, high_length=80, max_length=150,
                   low_width=20, high_width=60, max_width=80)])

    def test_plant_size_25(self):
        """It gets sepal measurements with a sex notation."""
        self.assertEqual(
            PLANT_SIZE.parse('sepals (pistillate) linear, 6–7 mm;'),
            [Trait(start=0, end=34, units='mm',
                   part='sepals', sex='pistillate',
                   low_length=6, high_length=7)])

    def test_plant_size_26(self):
        """It skips over lobe notations."""
        self.assertEqual(
            PLANT_SIZE.parse(
                'blade suborbiculate to depressed-ovate, palmately 5-lobed, '
                'sinuses 1/2–2/3 to petiole, 3–7 × 4–10 cm, usually broader '
                'than long '),
            [Trait(start=78, end=100, part='petiole', units='cm',
                   low_length=30.0, high_length=70.0,
                   low_width=40.0, high_width=100.0)])

    def test_plant_size_27(self):
        """It allows spaces in measurements."""
        self.assertEqual(
            PLANT_SIZE.parse('Leaves: petiole 1.5-7.5 (-12) cm'),
            [Trait(start=8, end=32, part='petiole', units='cm',
                   low_length=15.0, high_length=75.0, max_length=120.0)])

    def test_plant_size_28(self):
        """It handles a diameter as a dimension."""
        self.assertEqual(
            PLANT_SIZE.parse('Flowers 5–10 cm diam.; hypanthium 4–8 mm,'),
            [Trait(start=0, end=20, units='cm',
                   dimension='diam', part='flowers',
                   low_length=50.0, high_length=100.0),
             Trait(start=23, end=40, units='mm', part='hypanthium',
                   low_length=4.0, high_length=8.0)])

    def test_plant_size_29(self):
        """It handles ranges for hypanthium notations."""
        self.assertEqual(
            PLANT_SIZE.parse('hypanthium cupulate, 5–8 mm;'),
            [Trait(start=0, end=27, part='hypanthium', units='mm',
                   low_length=5, high_length=8)])

    def test_plant_size_30(self):
        """It handles a cross notation for seed sizes."""
        self.assertEqual(
            PLANT_SIZE.parse('Seeds brown, oblong, obovoid, or subglobose, '
                             'ca. 0.6 × 0.3-0.5 mm, wingless;'),
            [Trait(start=0, end=65, part='seeds', units='mm',
                   low_length=0.6, low_width=0.3, high_width=0.5)])
