"""Test attaching traits to plant parts."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from tests.setup import test


class TestAttach(unittest.TestCase):
    """Test attaching traits to plant parts."""

    def test_attach_01(self):
        self.assertEqual(
            test('leaves and yellow petals.'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'yellow',
              'trait': 'color', 'part': 'petal', 'start': 11, 'end': 17},
             {'part': 'petal', 'trait': 'part', 'start': 18, 'end': 24}]
        )

    def test_attach_02(self):
        self.assertEqual(
            test('perianth lobes elliptic, ca. 1 mm'),
            [{'part': 'perianth', 'trait': 'part', 'start': 0, 'end': 8},
             {'subpart': 'lobe', 'part': 'perianth', 'trait': 'subpart',
              'start': 9, 'end': 14},
             {'shape': 'elliptic', 'trait': 'shape', 'part': 'perianth',
              'subpart': 'lobe', 'start': 15,
              'end': 23},
             {'length_low': 1, 'length_units': 'mm',
              'trait': 'size', 'part': 'perianth', 'subpart': 'lobe',
              'start': 25, 'end': 33}]
        )

    def test_attach_03(self):
        self.assertEqual(
            test('fruits (1--)3-lobed,'),
            [{'part': 'fruit', 'trait': 'part', 'start': 0, 'end': 6},
             {'min': 1, 'low': 3, 'trait': 'count', 'part': 'fruit',
              'subpart': 'lobe', 'start': 7,
              'end': 19}]
        )

    def test_attach_04(self):
        self.assertEqual(
            test('petals spreading, pink, unlobed,'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'pink', 'trait': 'color', 'part': 'petal', 'start': 18,
              'end': 22},
             {'start': 24, 'end': 31, 'min': 0, 'trait': 'count',
              'part': 'petal', 'subpart': 'lobe'}]
        )

    def test_attach_05(self):
        self.assertEqual(
            test('Inflorescences 10+-flowered'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 14},
             {'low': 10, 'indefinite': True,
              'trait': 'count', 'part': 'inflorescence', 'subpart': 'flowered',
              'start': 15, 'end': 27}]
        )

    def test_attach_06(self):
        self.assertEqual(
            test('blade [3–5-foliolate]'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'low': 3, 'high': 5, 'trait': 'count', 'part': 'leaflet',
              'start': 6, 'end': 21}]
        )

    def test_attach_07(self):
        self.assertEqual(
            test('Racemes sessile, 2- or 3-flowered'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 7},
             {'low': 2, 'high': 3,
              'trait': 'count', 'part': 'inflorescence', 'subpart': 'flowered',
              'start': 17, 'end': 33}]
        )

    def test_attach_08(self):
        self.assertEqual(
            test('Legumes with a slender stipe 2-5 mm, 10-12 mm, ca. '
                 '4 mm high and ca. 3 mm wide, '),
            [{'part': 'legume', 'trait': 'part', 'start': 0, 'end': 7},
             {'subpart': 'stipe', 'part': 'legume', 'trait': 'subpart',
              'start': 23, 'end': 28},
             {'length_low': 2, 'length_high': 5, 'length_units': 'mm',
              'trait': 'size', 'part': 'legume', 'subpart': 'stipe',
              'start': 29, 'end': 35},
             {'length_low': 10, 'length_high': 12, 'length_units': 'mm',
              'trait': 'size', 'part': 'legume', 'start': 37, 'end': 45},
             {'height_low': 4, 'height_units': 'mm', 'trait': 'size',
              'part': 'legume',
              'start': 47, 'end': 60},
             {'width_low': 3, 'width_units': 'mm', 'trait': 'size',
              'part': 'legume',
              'start': 65, 'end': 78}]
        )

    def test_attach_09(self):
        self.assertEqual(
            test('Petals purple, keel with blue tip; standard 8-9 × ca. 6 mm, '
                 'widely elliptic, emarginate;'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'purple',
              'trait': 'color', 'part': 'petal', 'start': 7, 'end': 13},
             {'subpart': 'keel', 'part': 'petal', 'trait': 'subpart',
              'start': 15, 'end': 19},
             {'color': 'blue-tip',
              'trait': 'color', 'part': 'petal', 'subpart': 'keel',
              'start': 25, 'end': 33},
             {'length_low': 8, 'length_high': 9,
              'width_low': 6, 'width_units': 'mm',
              'trait': 'size', 'part': 'petal', 'start': 44, 'end': 58},
             {'shape': 'elliptic',
              'trait': 'shape', 'part': 'petal', 'start': 67, 'end': 75},
             {'shape': 'emarginate',
              'trait': 'shape', 'part': 'petal', 'start': 77, 'end': 87}]
        )

    def test_attach_10(self):
        self.assertEqual(
            test("""
                Calyx ca. 5 mm, loosely to rather densely appressed hairy;
                teeth ca. 2.5 mm.
                """),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 5,
              'length_units': 'mm',
              'trait': 'size', 'part': 'calyx',
              'start': 6,
              'end': 14},
             {'subpart': 'tooth', 'part': 'calyx', 'trait': 'subpart',
              'start': 59, 'end': 64},
             {'length_low': 2.5,
              'length_units': 'mm',
              'trait': 'size', 'part': 'calyx', 'subpart': 'tooth',
              'start': 65,
              'end': 75}]
        )

    def test_attach_11(self):
        self.assertEqual(
            test("""
                Plants to 30 cm tall, strongly branched, with appressed to
                spreading only white hairs 0.2-1.5 mm, at calyx up to 3 mm.
                """),
            [{'part': 'plant', 'trait': 'part', 'start': 0, 'end': 6},
             {'height_high': 30, 'height_units': 'cm',
              'trait': 'size', 'part': 'plant', 'start': 7, 'end': 20},
             {'color': 'white',
              'trait': 'color', 'part': 'plant', 'subpart': 'hair',
              'start': 74, 'end': 79},
             {'subpart': 'hair', 'part': 'plant', 'trait': 'subpart',
              'start': 80, 'end': 85},
             {'length_low': 0.2, 'length_high': 1.5, 'length_units': 'mm',
              'trait': 'size', 'part': 'plant', 'subpart': 'hair', 'start': 86,
              'end': 96},
             {'length_high': 3, 'length_units': 'mm',
              'trait': 'size', 'part': 'plant', 'subpart': 'hair',
              'start': 110, 'end': 117}]
        )

    def test_attach_12(self):
        self.assertEqual(
            test("""
                Calyx shortly tubular, 8-9 mm, subglabrous or in upper part
                with short spreading black hairs; teeth nearly equal, narrowly
                triangular, 0.8-1 mm."""),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'shape': 'tubular',
              'trait': 'shape', 'part': 'calyx', 'start': 14, 'end': 21},
             {'length_low': 8, 'length_high': 9, 'length_units': 'mm',
              'trait': 'size', 'part': 'calyx', 'start': 23, 'end': 29},
             {'color': 'black',
              'trait': 'color', 'part': 'calyx', 'subpart': 'hair',
              'start': 81, 'end': 86},
             {'subpart': 'hair', 'part': 'calyx', 'trait': 'subpart',
              'start': 87, 'end': 92},
             {'subpart': 'tooth', 'part': 'calyx', 'trait': 'subpart',
              'start': 94, 'end': 99},
             {'shape': 'triangular',
              'trait': 'shape', 'part': 'calyx', 'subpart': 'tooth',
              'start': 114, 'end': 133},
             {'length_low': 0.8, 'length_high': 1.0, 'length_units': 'mm',
              'trait': 'size', 'part': 'calyx', 'subpart': 'tooth',
              'start': 135, 'end': 143}]
        )

    def test_attach_13(self):
        self.assertEqual(
            test("""
                Calyx 10-12 mm, densely covered with extremely asymmetrically
                bifurcate to basifixed, spreading hairs 1-2 mm; teeth ca.
                4 mm. Petals white; standard oblong-pandurate, ca. 25 × 8 mm,
                in lower 1/3 slightly constricted, base widened,
                hastate-auriculate, apex emarginate;"""),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'part': 'calyx',
              'length_low': 10, 'length_high': 12, 'length_units': 'mm',
              'trait': 'size', 'start': 6, 'end': 14},
             {'part': 'calyx', 'subpart': 'hair',
              'trait': 'subpart', 'start': 96, 'end': 101},
             {'part': 'calyx', 'subpart': 'hair',
              'length_low': 1, 'length_high': 2, 'length_units': 'mm',
              'trait': 'size', 'start': 102, 'end': 108},
             {'part': 'calyx', 'subpart': 'tooth',
              'trait': 'subpart', 'start': 110, 'end': 115},
             {'part': 'calyx', 'subpart': 'tooth',
              'length_low': 4, 'length_units': 'mm',
              'trait': 'size', 'start': 116, 'end': 124},
             {'part': 'petal', 'trait': 'part', 'start': 126, 'end': 132},
             {'color': 'white', 'trait': 'color', 'start': 133, 'end': 138},
             {'shape': 'oblong-pandurate', 'trait': 'shape', 'start': 149, 'end': 165},
             {'length_low': 25, 'width_low': 8, 'width_units': 'mm',
              'trait': 'size', 'start': 167, 'end': 180},
             {'subpart': 'base', 'trait': 'subpart', 'start': 217, 'end': 221},
             {'shape': 'hastate-auriculate',
              'trait': 'shape', 'start': 231, 'end': 249},
             {'subpart': 'apex', 'trait': 'subpart', 'start': 251, 'end': 255},
             {'shape': 'emarginate', 'trait': 'shape', 'start': 256, 'end': 266}]
        )

    def test_attach_14(self):
        self.assertEqual(
            test("""
                Racemes short, 3-9-flowered; peduncle 0.5-2 cm, loosely to
                rather densely hairy; bracts 0.5-1 mm, white hairy."""),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 7},
             {'low': 3, 'high': 9,
              'trait': 'count', 'part': 'inflorescence', 'subpart': 'flowered',
              'start': 15, 'end': 27},
             {'part': 'peduncle', 'trait': 'part', 'start': 29, 'end': 37},
             {'length_low': 0.5, 'length_high': 2.0, 'length_units': 'cm',
              'trait': 'size', 'part': 'peduncle', 'start': 38, 'end': 46},
             {'part': 'bract', 'trait': 'part', 'start': 81, 'end': 87},
             {'length_low': 0.5, 'length_high': 1.0, 'length_units': 'mm',
              'trait': 'size', 'part': 'bract', 'start': 88, 'end': 96},
             {'color': 'white', 'trait': 'color', 'part': 'bract',
              'start': 98, 'end': 103}]
        )

    def test_attach_15(self):
        self.assertEqual(
            test('hypanthium pistillodes with 3-lobed ovary.'),
            [{'part': 'hypanthium', 'trait': 'part', 'start': 0, 'end': 10},
             {'part': 'pistil', 'trait': 'part', 'start': 11, 'end': 22},
             {'low': 3, 'trait': 'count', 'part': 'ovary', 'subpart': 'lobe',
              'start': 28, 'end': 35},
             {'part': 'ovary', 'trait': 'part', 'start': 36, 'end': 41}]
        )

    def test_attach_16(self):
        self.assertEqual(
            test('roots thin, without thick, woody rootstock'),
            [{'part': 'root', 'trait': 'part', 'start': 0, 'end': 5},
             {'woodiness': 'not woody',
              'trait': 'woodiness', 'part': 'rootstock', 'start': 12,
              'end': 32},
             {'part': 'rootstock', 'trait': 'part', 'start': 33, 'end': 42}]
        )

    def test_attach_17(self):
        self.assertEqual(
            test("""
                Legumes with a stipe 6-7 mm, pen­dulous, narrowly ellipsoid,
                1.5-2.4 cm, 6-7 mm wide and 4-5 mm high,"""),
            [{'part': 'legume', 'trait': 'part', 'start': 0, 'end': 7},
             {'subpart': 'stipe', 'part': 'legume', 'trait': 'subpart',
              'start': 15, 'end': 20},
             {'length_low': 6, 'length_high': 7, 'length_units': 'mm',
              'trait': 'size', 'part': 'legume', 'subpart': 'stipe',
              'start': 21, 'end': 27},
             {'shape': 'ellipsoid',
              'trait': 'shape', 'part': 'legume', 'start': 41, 'end': 59},
             {'length_low': 1.5, 'length_high': 2.4, 'length_units': 'cm',
              'trait': 'size', 'part': 'legume', 'start': 61, 'end': 71},
             {'width_low': 6, 'width_high': 7, 'width_units': 'mm',
              'trait': 'size', 'part': 'legume', 'start': 73, 'end': 84},
             {'height_low': 4, 'height_high': 5, 'height_units': 'mm',
              'trait': 'size', 'part': 'legume', 'start': 89, 'end': 100}]
        )

    def test_attach_18(self):
        self.assertEqual(
            test('Leaves 1.5-3 cm; leaflets 2-6 × 1-1.5 mm, with hairs ca. 1 mm.'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'length_low': 1.5, 'length_high': 3.0, 'length_units': 'cm',
              'trait': 'size', 'part': 'leaf', 'start': 7, 'end': 15},
             {'part': 'leaflet', 'trait': 'part', 'start': 17, 'end': 25},
             {'length_low': 2, 'length_high': 6,
              'width_low': 1.0, 'width_high': 1.5, 'width_units': 'mm',
              'trait': 'size', 'part': 'leaflet', 'start': 26, 'end': 40},
             {'subpart': 'hair', 'part': 'leaflet', 'trait': 'subpart',
              'start': 47, 'end': 52},
             {'length_low': 1, 'length_units': 'mm',
              'trait': 'size', 'part': 'leaflet', 'subpart': 'hair',
              'start': 53, 'end': 61}]
        )

    def test_attach_19(self):
        self.assertEqual(
            test("""
                Calyx 7-8 mm, rather densely covered with ± medifixed,
                subappressed, flexuous, black hairs 0.5-1 mm,
                """),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 7, 'length_high': 8, 'length_units': 'mm',
              'trait': 'size', 'part': 'calyx', 'start': 6, 'end': 12},
             {'color': 'black',
              'trait': 'color', 'part': 'calyx', 'subpart': 'hair',
              'start': 79, 'end': 84},
             {'subpart': 'hair', 'part': 'calyx', 'trait': 'subpart',
              'start': 85, 'end': 90},
             {'length_low': 0.5, 'length_high': 1.0, 'length_units': 'mm',
              'trait': 'size', 'part': 'calyx', 'subpart': 'hair', 'start': 91,
              'end': 99}]
        )

    def test_attach_20(self):
        self.assertEqual(
            test('Plants acaulescent, covered with mostly medifixed white hairs'),
            [{'part': 'plant', 'trait': 'part', 'start': 0, 'end': 6},
             {'habit': 'acaulescent',
              'trait': 'habit', 'part': 'plant', 'start': 7, 'end': 18},
             {'color': 'white',
              'trait': 'color', 'part': 'plant', 'subpart': 'hair',
              'start': 50, 'end': 55},
             {'subpart': 'hair', 'part': 'plant', 'trait': 'subpart',
              'start': 56, 'end': 61}]
        )

    def test_attach_21(self):
        self.assertEqual(
            test("""
                leaflets in 7-9 pairs, widely obovate to suborbicular,
                4-6 × 3.5-5.5 mm, abaxially rather densely and adaxially
                sparsely to loosely covered with symmetrically or
                asymmetrically, partly flexuous, ascending to spreading,
                white hairs
                """),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'low': 7, 'high': 9, 'group': 'pairs',
              'trait': 'count', 'part': 'leaflet', 'start': 12, 'end': 21},
             {'shape': 'obovate',
              'trait': 'shape', 'part': 'leaflet', 'start': 30, 'end': 37},
             {'shape': 'orbicular',
              'trait': 'shape', 'part': 'leaflet', 'start': 41, 'end': 53},
             {'length_low': 4, 'length_high': 6,
              'width_low': 3.5, 'width_high': 5.5, 'width_units': 'mm',
              'trait': 'size', 'part': 'leaflet', 'start': 55, 'end': 71},
             {'color': 'white',
              'trait': 'color', 'part': 'leaflet', 'subpart': 'hair',
              'start': 219, 'end': 224},
             {'subpart': 'hair', 'part': 'leaflet', 'trait': 'subpart',
              'start': 225, 'end': 230}]
        )

    def test_attach_22(self):
        self.assertEqual(
            test("""
                 Legumes with a stipe 6-7 mm, pen­dulous, narrowly ellipsoid,
                 1.5-2.4 cm, 6-7 mm wide and 4-5 mm high, with a beak ca. 2 mm;
                 valves membranous, rather densely covered
                 with very short white and black nearly ap­pressed hairs.
                """),
            [{'part': 'legume', 'trait': 'part', 'start': 0, 'end': 7},
             {'subpart': 'stipe', 'part': 'legume', 'trait': 'subpart',
              'start': 15, 'end': 20},
             {'length_low': 6, 'length_high': 7, 'length_units': 'mm',
              'trait': 'size', 'part': 'legume', 'subpart': 'stipe',
              'start': 21, 'end': 27},
             {'shape': 'ellipsoid', 'trait': 'shape', 'part': 'legume',
              'start': 41,
              'end': 59},
             {'length_low': 1.5, 'length_high': 2.4, 'length_units': 'cm',
              'trait': 'size', 'part': 'legume', 'start': 61, 'end': 71},
             {'width_low': 6, 'width_high': 7, 'width_units': 'mm',
              'trait': 'size', 'part': 'legume', 'start': 73, 'end': 84},
             {'height_low': 4, 'height_high': 5, 'height_units': 'mm',
              'trait': 'size', 'part': 'legume', 'start': 89, 'end': 100},
             {'subpart': 'beak', 'part': 'legume', 'trait': 'subpart',
              'start': 109, 'end': 113},
             {'length_low': 2, 'length_units': 'mm',
              'trait': 'size', 'part': 'legume', 'subpart': 'beak',
              'start': 114, 'end': 122},
             {'color': 'white',
              'trait': 'color', 'part': 'legume', 'subpart': 'hair',
              'start': 182, 'end': 187},
             {'color': 'black',
              'trait': 'color', 'part': 'legume', 'subpart': 'hair',
              'start': 192, 'end': 197},
             {'subpart': 'hair', 'part': 'legume', 'trait': 'subpart',
              'start': 216, 'end': 221}]
        )

    def test_attach_23(self):
        self.assertEqual(
            test("""
                 leaflets in 3-5 pairs, surfaces with minute blackish dots
                 often only in basal 1/2, rounded at apex.
                """),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'low': 3, 'high': 5, 'group': 'pairs',
              'trait': 'count', 'part': 'leaflet', 'start': 12, 'end': 21},
             {'subpart': 'surface',
              'part': 'leaflet', 'trait': 'subpart', 'start': 23, 'end': 31},
             {'color': 'black-dots',
              'trait': 'color', 'part': 'leaflet', 'subpart': 'surface',
              'start': 44, 'end': 57},
             {'location': 'basal',
              'trait': 'location', 'part': 'leaflet', 'subpart': 'surface',
              'start': 72, 'end': 77},
             {'shape': 'orbicular',
              'trait': 'shape', 'part': 'leaflet', 'subpart': 'apex',
              'start': 83, 'end': 90},
             {'subpart': 'apex', 'part': 'leaflet', 'trait': 'subpart',
              'start': 94, 'end': 98}]
        )

    def test_attach_24(self):
        self.assertEqual(
            test("""
                 Calyx 7-8 mm, rather densely covered
                 with ± medifixed, subappressed, flexuous, black hairs
                 0.5-1 mm,
                 with some longer, ascending, white and black hairs mixed in;
                """),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 7, 'length_high': 8, 'length_units': 'mm',
              'trait': 'size', 'part': 'calyx', 'start': 6, 'end': 12},
             {'color': 'black',
              'trait': 'color', 'part': 'calyx', 'subpart': 'hair',
              'start': 79, 'end': 84},
             {'subpart': 'hair', 'part': 'calyx', 'trait': 'subpart',
              'start': 85, 'end': 90},
             {'length_low': 0.5, 'length_high': 1.0, 'length_units': 'mm',
              'trait': 'size', 'part': 'calyx', 'subpart': 'hair', 'start': 91,
              'end': 99},
             {'color': 'white',
              'trait': 'color', 'part': 'calyx', 'subpart': 'hair',
              'start': 130, 'end': 135},
             {'color': 'black',
              'trait': 'color', 'part': 'calyx', 'subpart': 'hair',
              'start': 140, 'end': 145},
             {'subpart': 'hair', 'part': 'calyx', 'trait': 'subpart',
              'start': 146, 'end': 151}]
        )

    def test_attach_25(self):
        self.assertEqual(
            test("""
                 Legumes curved, 9-12 mm, 2.5-3 mm high, keeled ven­trally;
                 valves with long, ascending, white hairs.
                """),
            [{'part': 'legume', 'trait': 'part', 'start': 0, 'end': 7},
             {'shape': 'curved',
              'trait': 'shape', 'part': 'legume', 'start': 8, 'end': 14},
             {'length_low': 9, 'length_high': 12, 'length_units': 'mm',
              'trait': 'size', 'part': 'legume', 'start': 16, 'end': 23},
             {'height_low': 2.5, 'height_high': 3.0, 'height_units': 'mm',
              'trait': 'size', 'part': 'legume', 'start': 25, 'end': 38},
             {'shape': 'keeled',
              'trait': 'shape', 'part': 'legume', 'start': 40, 'end': 46},
             {'color': 'white',
              'trait': 'color', 'part': 'legume', 'subpart': 'hair',
              'start': 88, 'end': 93},
             {'subpart': 'hair', 'part': 'legume', 'trait': 'subpart',
              'start': 94, 'end': 99}]
        )

    def test_attach_26(self):
        self.assertEqual(
            test("""
                 Plants 4-20 cm tall, acaulescent, with white or reddish when
                 mature hairs up to 3 mm.
                """),
            [{'part': 'plant', 'trait': 'part', 'start': 0, 'end': 6},
             {'height_low': 4, 'height_high': 20, 'height_units': 'cm',
              'trait': 'size', 'part': 'plant', 'start': 7, 'end': 19},
             {'habit': 'acaulescent',
              'trait': 'habit', 'part': 'plant', 'start': 21, 'end': 32},
             {'color': 'white',
              'trait': 'color', 'part': 'plant', 'subpart': 'hair',
              'start': 39, 'end': 44},
             {'color': 'red',
              'trait': 'color', 'part': 'plant', 'subpart': 'hair',
              'start': 48, 'end': 55},
             {'subpart': 'hair', 'part': 'plant', 'trait': 'subpart',
              'start': 68, 'end': 73},
             {'length_high': 3, 'length_units': 'mm',
              'trait': 'size', 'part': 'plant', 'subpart': 'hair',
              'start': 77, 'end': 84}]
        )

    def test_attach_27(self):
        self.assertEqual(
            test("""
                 Plants with white hairs, near stipules and in inflorescence
                 also black hairy.
                """),
            [{'part': 'plant', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'white',
              'trait': 'color', 'part': 'plant', 'subpart': 'hair',
              'start': 12, 'end': 17},
             {'subpart': 'hair', 'part': 'plant', 'trait': 'subpart',
              'start': 18, 'end': 23},
             {'color': 'black',
              'trait': 'color', 'part': 'plant', 'start': 65, 'end': 70}]
        )

    def test_attach_28(self):
        self.assertEqual(
            test("""
                 Petals yellow, standard and keel often suffused with violet;
                 apex retuse
                """),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'yellow',
              'trait': 'color', 'part': 'petal', 'start': 7, 'end': 13},
             {'subpart': 'keel', 'part': 'petal', 'trait': 'subpart',
              'start': 28, 'end': 32},
             {'color': 'purple',
              'trait': 'color', 'part': 'petal', 'subpart': 'keel',
              'start': 53, 'end': 59},
             {'subpart': 'apex', 'part': 'petal', 'trait': 'subpart',
              'start': 61, 'end': 65},
             {'shape': 'retuse',
              'trait': 'shape', 'part': 'petal', 'subpart': 'apex',
              'start': 66, 'end': 72}]
        )

    def test_attach_29(self):
        self.assertEqual(
            test('limbs with basal abaxial edges'),
            [{'subpart': 'limb', 'trait': 'subpart',
              'start': 0, 'end': 5},
             {'location': 'basal',
              'trait': 'location', 'part': 'plant', 'subpart': 'limb',
              'start': 11, 'end': 16},
             {'location': 'abaxial',
              'trait': 'location', 'part': 'plant', 'subpart': 'limb',
              'start': 17, 'end': 24}]
        )
