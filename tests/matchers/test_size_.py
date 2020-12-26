"""Test plant size trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from tests.setup import test_efloras


class TestSize(unittest.TestCase):
    """Test plant size trait parsers."""

    def test_size_01(self):
        self.assertEqual(
            test_efloras('Leaf (12-)23-34 × 45-56 cm'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'length_min': 12, 'length_low': 23, 'length_high': 34,
              'width_low': 45, 'width_high': 56, 'width_units': 'cm',
              'trait': 'size', 'part': 'leaf',
              'start': 5, 'end': 26}]
        )

    def test_size_02(self):
        self.assertEqual(
            test_efloras('leaf (12-)23-34 × 45-56'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4}]
        )

    def test_size_03(self):
        self.assertEqual(
            test_efloras('blade 1.5–5(–7) cm'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 1.5,
              'length_high': 5.0,
              'length_max': 7.0,
              'length_units': 'cm',
              'trait': 'size', 'part': 'leaf',
              'start': 6,
              'end': 18}]
        )

    def test_size_04(self):
        self.assertEqual(
            test_efloras('leaf shallowly to deeply 5–7-lobed'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'low': 5, 'high': 7, 'trait': 'count', 'part': 'leaf',
              'subpart': 'lobe', 'start': 25, 'end': 34}]
        )

    def test_size_05(self):
        self.assertEqual(
            test_efloras('leaf 4–10 cm wide'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'width_low': 4,
              'width_high': 10,
              'width_units': 'cm',
              'trait': 'size', 'part': 'leaf',
              'start': 5,
              'end': 17}]
        )

    def test_size_06(self):
        self.assertEqual(
            test_efloras('leaf sinuses 1/5–1/4 to base'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'subpart': 'sinus', 'trait': 'subpart',
              'part': 'leaf', 'start': 5, 'end': 12},
             {'subpart': 'base', 'trait': 'subpart',
              'part': 'leaf', 'start': 24, 'end': 28}]
        )

    def test_size_07(self):
        self.assertEqual(
            test_efloras('petiolules 2–5 mm'),
            [{'part': 'petiole', 'trait': 'part', 'start': 0, 'end': 10},
             {'length_low': 2,
              'length_high': 5,
              'length_units': 'mm',
              'trait': 'size', 'part': 'petiole',
              'start': 11,
              'end': 17}]
        )

    def test_size_08(self):
        self.assertEqual(
            test_efloras(
                'petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm.'),
            [{'part': 'petiole', 'trait': 'part', 'start': 0, 'end': 10},
             {'length_low': 2,
              'length_high': 5,
              'length_units': 'mm',
              'trait': 'size', 'part': 'petiole',
              'start': 11, 'end': 17},
             {'margin_shape': 'serrate',
              'trait': 'margin_shape', 'part': 'petiole',
              'start': 19, 'end': 35},
             {'part': 'petiole', 'trait': 'part', 'start': 37, 'end': 45},
             {'length_low': 16,
              'length_high': 28,
              'length_units': 'mm',
              'trait': 'size', 'part': 'petiole',
              'start': 46, 'end': 54}]
        )

    def test_size_09(self):
        self.assertEqual(
            test_efloras('Leaves: petiole 2–15 cm;'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'part': 'petiole', 'trait': 'part', 'start': 8, 'end': 15},
             {'length_low': 2,
              'length_high': 15,
              'length_units': 'cm',
              'trait': 'size', 'part': 'petiole',
              'start': 16,
              'end': 23}]
        )

    def test_size_10(self):
        self.assertEqual(
            test_efloras('petiole [5–]7–25[–32] mm, glabrous,'),
            [{'part': 'petiole', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_min': 5,
              'length_low': 7,
              'length_high': 25,
              'length_max': 32,
              'length_units': 'mm',
              'trait': 'size', 'part': 'petiole',
              'start': 8,
              'end': 24}]
        )

    def test_size_11(self):
        self.assertEqual(
            test_efloras('leaf 2–4 cm × 2–10 mm'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'length_low': 2,
              'length_high': 4,
              'length_units': 'cm',
              'width_low': 2,
              'width_high': 10,
              'width_units': 'mm',
              'trait': 'size', 'part': 'leaf',
              'start': 5,
              'end': 21}]
        )

    def test_size_12(self):
        self.assertEqual(
            test_efloras('leaf deeply to shallowly lobed, 4–5(–7) cm wide,'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'width_low': 4, 'width_high': 5, 'width_max': 7,
              'width_units': 'cm',
              'trait': 'size', 'part': 'leaf', 'start': 32, 'end': 47}]
        )

    def test_size_13(self):
        self.assertEqual(
            test_efloras(
                'Leaves 3-foliolate, lateral pair of leaflets '
                'deeply lobed, petiolules 2–5 mm,'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'low': 3, 'trait': 'count', 'part': 'leaflet',
              'start': 7, 'end': 18},
             {'location': 'lateral', 'group': 'pair', 'part': 'leaflet',
              'trait': 'part', 'start': 20, 'end': 44},
             {'part': 'petiole',
              'trait': 'part', 'start': 59, 'end': 69},
             {'length_low': 2, 'length_high': 5, 'length_units': 'mm',
              'trait': 'size', 'part': 'petiole', 'start': 70, 'end': 76}]
        )

    def test_size_14(self):
        self.assertEqual(
            test_efloras('terminal leaflet 3–5 cm, blade petiolule 3–12 mm,'),
            [{'location': 'terminal', 'part': 'leaflet',
              'trait': 'part', 'start': 0, 'end': 16},
             {'length_low': 3, 'length_high': 5, 'length_units': 'cm',
              'location': 'terminal',
              'trait': 'size', 'part': 'leaflet', 'start': 17, 'end': 23},
             {'part': 'leaf', 'trait': 'part', 'start': 25, 'end': 30},
             {'part': 'petiole', 'trait': 'part', 'start': 31, 'end': 40},
             {'length_low': 3, 'length_high': 12, 'length_units': 'mm',
              'trait': 'size', 'part': 'petiole', 'start': 41, 'end': 48}]
        )

    def test_size_15(self):
        self.assertEqual(
            test_efloras(
                'leaf shallowly 3–5(–7)-lobed, 5–25 × (8–)10–25(–30) cm,'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'low': 3, 'high': 5, 'max': 7,
              'trait': 'count', 'part': 'leaf', 'subpart': 'lobe',
              'start': 15, 'end': 28},
             {'length_low': 5, 'length_high': 25, 'width_min': 8,
              'width_low': 10, 'width_high': 25, 'width_max': 30,
              'width_units': 'cm',
              'trait': 'size', 'part': 'leaf', 'start': 30, 'end': 54}]
        )

    def test_size_16(self):
        self.assertEqual(
            test_efloras('(3–)5-lobed, 6–20(–30) × 6–25 cm,'),
            [{'min': 3, 'low': 5, 'trait': 'count', 'part': 'plant',
              'subpart': 'lobe', 'start': 0, 'end': 11},
             {'length_low': 6,
              'length_high': 20,
              'length_max': 30,
              'width_low': 6,
              'width_high': 25,
              'width_units': 'cm',
              'trait': 'size', 'part': 'plant',
              'start': 13,
              'end': 32}]
        )

    def test_size_17(self):
        self.assertEqual(
            test_efloras('petiole to 11 cm;'),
            [{'part': 'petiole', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_high': 11,
              'length_units': 'cm',
              'trait': 'size', 'part': 'petiole',
              'start': 8,
              'end': 16}]
        )

    def test_size_18(self):
        self.assertEqual(
            test_efloras(
                'petals (1–)3–10(–12) mm (pistillate) '
                'or 5–8(–10) mm (staminate)'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'length_min': 1,
              'length_low': 3,
              'length_high': 10,
              'length_max': 12,
              'length_units': 'mm',
              'sex': 'pistillate',
              'trait': 'size', 'part': 'petal',
              'start': 7,
              'end': 36},
             {'length_low': 5,
              'length_high': 8,
              'length_max': 10,
              'length_units': 'mm',
              'sex': 'staminate',
              'trait': 'size', 'part': 'petal',
              'start': 40,
              'end': 63}]
        )

    def test_size_19(self):
        self.assertEqual(
            test_efloras('Flowers 5–10 cm diam.; hypanthium 4–8 mm,'),
            [{'part': 'flower', 'trait': 'part', 'start': 0, 'end': 7},
             {'diameter_low': 5,
              'diameter_high': 10,
              'diameter_units': 'cm',
              'trait': 'size', 'part': 'flower',
              'start': 8,
              'end': 20},
             {'part': 'hypanthium', 'trait': 'part', 'start': 23, 'end': 33},
             {'length_low': 4,
              'length_high': 8,
              'length_units': 'mm',
              'trait': 'size', 'part': 'hypanthium',
              'start': 34,
              'end': 40}]
        )

    def test_size_20(self):
        self.assertEqual(
            test_efloras('Flowers 5--16 × 4--12 cm'),
            [{'part': 'flower', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_low': 5,
              'length_high': 16,
              'width_low': 4,
              'width_high': 12,
              'width_units': 'cm',
              'trait': 'size', 'part': 'flower',
              'start': 8,
              'end': 24}]
        )

    def test_size_21(self):
        self.assertEqual(
            test_efloras(
                'Inflorescences formed season before flowering and exposed '
                'during winter; staminate catkins 3--8.5 cm,'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 14},
             {'sex': 'male', 'part': 'catkin', 'trait': 'part',
              'start': 73, 'end': 90},
             {'sex': 'male', 'part': 'catkin',
              'length_low': 3.0, 'length_high': 8.5, 'length_units': 'cm',
              'trait': 'size', 'start': 91, 'end': 100}]
        )

    def test_size_22(self):
        self.assertEqual(
            test_efloras('Leaflets petiolulate; blade ovate, 8-15 × 4-15 cm,'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'part': 'leaf', 'trait': 'part', 'start': 22, 'end': 27},
             {'shape': 'ovate', 'trait': 'shape', 'part': 'leaf',
              'start': 28, 'end': 33},
             {'length_low': 8,
              'length_high': 15,
              'width_low': 4,
              'width_high': 15,
              'width_units': 'cm',
              'trait': 'size', 'part': 'leaf',
              'start': 35,
              'end': 49}]
        )

    def test_size_23(self):
        self.assertEqual(
            test_efloras('calyx, 8-10 mm, 3-4 mm high,'),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 8,
              'length_high': 10,
              'length_units': 'mm',
              'trait': 'size', 'part': 'calyx',
              'start': 7,
              'end': 14},
             {'height_low': 3,
              'height_high': 4,
              'height_units': 'mm',
              'trait': 'size', 'part': 'calyx',
              'start': 16,
              'end': 27}]
        )

    def test_size_24(self):
        self.assertEqual(
            test_efloras('Petals 15-21 × ca. 8 mm,'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'length_low': 15,
              'length_high': 21,
              'width_low': 8,
              'width_units': 'mm',
              'trait': 'size', 'part': 'petal',
              'start': 7,
              'end': 23}]
        )

    def test_size_25(self):
        self.assertEqual(
            test_efloras('Petals ca. 8 mm,'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'length_low': 8,
              'length_units': 'mm',
              'trait': 'size', 'part': 'petal',
              'start': 7,
              'end': 15}]
        )

    def test_size_26(self):
        self.assertEqual(
            test_efloras('Legumes 7-10 mm, 2.8-4.5 mm high and wide'),
            [{'part': 'legume', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_low': 7,
              'length_high': 10,
              'length_units': 'mm',
              'trait': 'size', 'part': 'legume',
              'start': 8,
              'end': 15},
             {'width_low': 2.8,
              'width_high': 4.5,
              'width_units': 'mm',
              'height_low': 2.8,
              'height_high': 4.5,
              'height_units': 'mm',
              'trait': 'size', 'part': 'legume',
              'start': 17,
              'end': 41}]
        )

    def test_size_27(self):
        self.assertEqual(
            test_efloras('Racemes 3-4 cm,'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_low': 3,
              'length_high': 4,
              'length_units': 'cm',
              'trait': 'size', 'part': 'inflorescence',
              'start': 8,
              'end': 14}]
        )

    def test_size_28(self):
        self.assertEqual(
            test_efloras(
                'Petals pale violet, with darker keel; standard '
                'elliptic, 6-7 × 3-4;'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'purple', 'trait': 'color', 'part': 'petal',
              'start': 12, 'end': 18},
             {'subpart': 'keel', 'trait': 'subpart',
              'part': 'petal', 'start': 32, 'end': 36},
             {'shape': 'elliptic', 'trait': 'shape', 'part': 'petal',
              'start': 47, 'end': 55}]
        )

    def test_size_29(self):
        self.assertEqual(
            test_efloras('Seeds ca. 1.6 × 1-1.3 × 0.7-0.8 cm; hilum 8-10 mm.'),
            [{'part': 'seed', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 1.6,
              'width_low': 1.0,
              'width_high': 1.3,
              'thickness_low': 0.7,
              'thickness_high': 0.8,
              'thickness_units': 'cm',
              'trait': 'size', 'part': 'seed',
              'start': 6,
              'end': 34},
             {'subpart': 'hilum', 'part': 'seed', 'trait': 'subpart',
              'start': 36, 'end': 41},
             {'length_low': 8,
              'length_high': 10,
              'length_units': 'mm',
              'trait': 'size', 'part': 'seed', 'subpart': 'hilum',
              'start': 42,
              'end': 49}]
        )

    def test_size_30(self):
        self.assertEqual(
            test_efloras('leaflets obovate, 1-2.5 × to 1.6 cm,'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'shape': 'obovate', 'trait': 'shape', 'part': 'leaflet',
              'start': 9, 'end': 16},
             {'length_low': 1.0, 'length_high': 2.5,
              'width_low': 1.6, 'width_units': 'cm',
              'trait': 'size', 'part': 'leaflet',
              'start': 18, 'end': 35}]
        )

    def test_size_31(self):
        self.assertEqual(
            test_efloras('Shrubs, 0.5–1[–2.5] m.'),
            [{'habit': 'shrub', 'trait': 'habit', 'part': 'plant',
              'start': 0, 'end': 6},
             {'length_low': 0.5, 'length_high': 1.0, 'length_max': 2.5,
              'length_units': 'm',
              'trait': 'size', 'part': 'plant',
              'start': 8, 'end': 22}]
        )

    def test_size_32(self):
        self.assertEqual(
            test_efloras('trunk to 3(?) cm d.b.h.;'),
            [{'part': 'trunk', 'trait': 'part', 'start': 0, 'end': 5},
             {'part': 'trunk',
              'dbh_high': 3, 'dbh_units': 'cm', 'uncertain': 'true',
              'trait': 'size', 'start': 6, 'end': 23}]
        )
