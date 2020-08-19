"""Test plant size trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from efloras.pylib.pipeline import parse


class TestSize(unittest.TestCase):
    """Test plant size trait parsers."""

    def test_size_01(self):
        self.assertEqual(
            parse('Leaf (12-)23-34 × 45-56 cm'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'length_min': 12,
              'length_low': 23,
              'length_high': 34,
              'width_low': 45,
              'width_high': 56,
              'width_units': 'cm',
              'trait': 'leaf_size',
              'start': 5,
              'end': 26}]
        )

    def test_size_02(self):
        self.assertEqual(
            parse('leaf (12-)23-34 × 45-56'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4}]
        )

    def test_size_03(self):
        self.assertEqual(
            parse('blade 1.5–5(–7) cm'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 1.5,
              'length_high': 5.0,
              'length_max': 7.0,
              'length_units': 'cm',
              'trait': 'leaf_size',
              'start': 6,
              'end': 18}]
        )

    def test_size_04(self):
        self.assertEqual(
            parse('leaf shallowly to deeply 5–7-lobed'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'low': 5, 'high': 7, 'trait': 'leaf_lobe_count', 'start': 25,
              'end': 34}]
        )

    def test_size_05(self):
        self.assertEqual(
            parse('leaf 4–10 cm wide'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'width_low': 4,
              'width_high': 10,
              'width_units': 'cm',
              'trait': 'leaf_size',
              'start': 5,
              'end': 17}]
        )

    def test_size_06(self):
        self.assertEqual(
            parse('leaf sinuses 1/5–1/4 to base'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'subpart': 'sinus', 'trait': 'subpart', 'start': 5, 'end': 12},
             {'subpart': 'base', 'trait': 'subpart', 'start': 24, 'end': 28}]
        )

    def test_size_07(self):
        self.assertEqual(
            parse('petiolules 2–5 mm'),
            [{'part': 'petiole', 'trait': 'part', 'start': 0, 'end': 10},
             {'length_low': 2,
              'length_high': 5,
              'length_units': 'mm',
              'trait': 'petiole_size',
              'start': 11,
              'end': 17}]
        )

    def test_size_08(self):
        self.assertEqual(
            parse('petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm.'),
            [{'part': 'petiole', 'trait': 'part', 'start': 0, 'end': 10},
             {'length_low': 2,
              'length_high': 5,
              'length_units': 'mm',
              'trait': 'petiole_size',
              'start': 11,
              'end': 17},
             {'margin_shape': 'serrate',
              'trait': 'petiole_margin_shape',
              'start': 19,
              'end': 35},
             {'part': 'petiole', 'trait': 'part', 'start': 37, 'end': 45},
             {'length_low': 16,
              'length_high': 28,
              'length_units': 'mm',
              'trait': 'petiole_size',
              'start': 46,
              'end': 54}]
        )

    def test_size_09(self):
        self.assertEqual(
            parse('Leaves: petiole 2–15 cm;'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'part': 'petiole', 'trait': 'part', 'start': 8, 'end': 15},
             {'length_low': 2,
              'length_high': 15,
              'length_units': 'cm',
              'trait': 'petiole_size',
              'start': 16,
              'end': 23}]
        )

    def test_size_10(self):
        self.assertEqual(
            parse('petiole [5–]7–25[–32] mm, glabrous,'),
            [{'part': 'petiole', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_min': 5,
              'length_low': 7,
              'length_high': 25,
              'length_max': 32,
              'length_units': 'mm',
              'trait': 'petiole_size',
              'start': 8,
              'end': 24}]
        )

    def test_size_11(self):
        self.assertEqual(
            parse('leaf 2–4 cm × 2–10 mm'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'length_low': 2,
              'length_high': 4,
              'length_units': 'cm',
              'width_low': 2,
              'width_high': 10,
              'width_units': 'mm',
              'trait': 'leaf_size',
              'start': 5,
              'end': 21}]
        )

    def test_size_12(self):
        self.assertEqual(
            parse('leaf deeply to shallowly lobed, 4–5(–7) cm wide,'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'width_low': 4,
              'width_high': 5,
              'width_max': 7,
              'width_units': 'cm',
              'trait': 'leaf_size',
              'start': 32,
              'end': 47}]
        )

    def test_size_13(self):
        self.assertEqual(
            parse(
                'Leaves 3-foliolate, lateral pair of leaflets '
                'deeply lobed, petiolules 2–5 mm,'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'low': 3, 'trait': 'leaf_count', 'start': 7, 'end': 18},
             {'location': 'lateral',
              'group': 'pair',
              'part': 'leaflet',
              'trait': 'part',
              'start': 20,
              'end': 44},
             {'part': 'petiole',
              'location': 'lateral',
              'trait': 'part',
              'start': 59,
              'end': 69},
             {'length_low': 2,
              'length_high': 5,
              'length_units': 'mm',
              'location': 'lateral',
              'trait': 'petiole_size',
              'start': 70,
              'end': 76}]
        )

    def test_size_14(self):
        self.assertEqual(
            parse('terminal leaflet 3–5 cm, blade petiolule 3–12 mm,'),
            [{'location': 'terminal',
              'part': 'leaflet',
              'trait': 'part',
              'start': 0,
              'end': 16},
             {'length_low': 3,
              'length_high': 5,
              'length_units': 'cm',
              'location': 'terminal',
              'trait': 'leaflet_size',
              'start': 17,
              'end': 23},
             {'part': 'leaf',
              'location': 'terminal',
              'trait': 'part',
              'start': 25,
              'end': 30},
             {'part': 'petiole',
              'location': 'terminal',
              'trait': 'part',
              'start': 31,
              'end': 40},
             {'length_low': 3,
              'length_high': 12,
              'length_units': 'mm',
              'location': 'terminal',
              'trait': 'petiole_size',
              'start': 41,
              'end': 48}]
        )

    def test_size_15(self):
        self.assertEqual(
            parse('leaf shallowly 3–5(–7)-lobed, 5–25 × (8–)10–25(–30) cm,'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 4},
             {'low': 3,
              'high': 5,
              'max': 7,
              'trait': 'leaf_lobe_count',
              'start': 15,
              'end': 28},
             {'length_low': 5,
              'length_high': 25,
              'width_min': 8,
              'width_low': 10,
              'width_high': 25,
              'width_max': 30,
              'width_units': 'cm',
              'trait': 'leaf_size',
              'start': 30,
              'end': 54}]
        )

    def test_size_16(self):
        self.assertEqual(
            parse('(3–)5-lobed, 6–20(–30) × 6–25 cm,'),
            [{'min': 3, 'low': 5, 'trait': 'plant_lobe_count', 'start': 0,
              'end': 11},
             {'length_low': 6,
              'length_high': 20,
              'length_max': 30,
              'width_low': 6,
              'width_high': 25,
              'width_units': 'cm',
              'trait': 'plant_size',
              'start': 13,
              'end': 32}]
        )

    def test_size_17(self):
        self.assertEqual(
            parse('petiole to 11 cm;'),
            [{'part': 'petiole', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_high': 11,
              'length_units': 'cm',
              'trait': 'petiole_size',
              'start': 8,
              'end': 16}]
        )

    def test_size_18(self):
        self.assertEqual(
            parse(
                'petals (1–)3–10(–12) mm (pistillate) '
                'or 5–8(–10) mm (staminate)'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'length_min': 1,
              'length_low': 3,
              'length_high': 10,
              'length_max': 12,
              'length_units': 'mm',
              'sex': 'pistillate',
              'trait': 'petal_size',
              'start': 7,
              'end': 36},
             {'length_low': 5,
              'length_high': 8,
              'length_max': 10,
              'length_units': 'mm',
              'sex': 'staminate',
              'trait': 'petal_size',
              'start': 40,
              'end': 63}]
        )

    def test_size_19(self):
        self.assertEqual(
            parse('Flowers 5–10 cm diam.; hypanthium 4–8 mm,'),
            [{'part': 'flower', 'trait': 'part', 'start': 0, 'end': 7},
             {'diameter_low': 5,
              'diameter_high': 10,
              'diameter_units': 'cm',
              'trait': 'flower_size',
              'start': 8,
              'end': 20},
             {'part': 'hypanthium', 'trait': 'part', 'start': 23, 'end': 33},
             {'length_low': 4,
              'length_high': 8,
              'length_units': 'mm',
              'trait': 'hypanthium_size',
              'start': 34,
              'end': 40}]
        )

    def test_size_20(self):
        self.assertEqual(
            parse('Flowers 5--16 × 4--12 cm'),
            [{'part': 'flower', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_low': 5,
              'length_high': 16,
              'width_low': 4,
              'width_high': 12,
              'width_units': 'cm',
              'trait': 'flower_size',
              'start': 8,
              'end': 24}]
        )

    def test_size_21(self):
        self.assertEqual(
            parse(
                'Inflorescences formed season before flowering and exposed '
                'during winter; staminate catkins in 1 or more clusters '
                'of 2--5, 3--8.5 cm,'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 14},
             {'low': 1, 'trait': 'inflorescence_count', 'start': 94,
              'end': 95},
             {'low': 2,
              'high': 5,
              'trait': 'inflorescence_count',
              'start': 116,
              'end': 120},
             {'length_low': 3.0,
              'length_high': 8.5,
              'length_units': 'cm',
              'trait': 'inflorescence_size',
              'start': 122,
              'end': 131}]
        )

    def test_size_22(self):
        self.assertEqual(
            parse('Leaflets petiolulate; blade ovate, 8-15 × 4-15 cm,'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'part': 'leaf', 'trait': 'part', 'start': 22, 'end': 27},
             {'shape': 'ovate', 'trait': 'leaf_shape', 'start': 28, 'end': 33},
             {'length_low': 8,
              'length_high': 15,
              'width_low': 4,
              'width_high': 15,
              'width_units': 'cm',
              'trait': 'leaf_size',
              'start': 35,
              'end': 49}]
        )

    def test_size_23(self):
        self.assertEqual(
            parse('calyx, 8-10 mm, 3-4 mm high,'),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 8,
              'length_high': 10,
              'length_units': 'mm',
              'trait': 'calyx_size',
              'start': 7,
              'end': 14},
             {'height_low': 3,
              'height_high': 4,
              'height_units': 'mm',
              'trait': 'calyx_size',
              'start': 16,
              'end': 27}]
        )

    def test_size_24(self):
        self.assertEqual(
            parse('Petals 15-21 × ca. 8 mm,'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'length_low': 15,
              'length_high': 21,
              'width_low': 8,
              'width_units': 'mm',
              'trait': 'petal_size',
              'start': 7,
              'end': 23}]
        )

    def test_size_25(self):
        self.assertEqual(
            parse('Petals ca. 8 mm,'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'length_low': 8,
              'length_units': 'mm',
              'trait': 'petal_size',
              'start': 7,
              'end': 15}]
        )

    def test_size_26(self):
        self.assertEqual(
            parse('Legumes 7-10 mm, 2.8-4.5 mm high and wide'),
            [{'part': 'legume', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_low': 7,
              'length_high': 10,
              'length_units': 'mm',
              'trait': 'legume_size',
              'start': 8,
              'end': 15},
             {'width_low': 2.8,
              'width_high': 4.5,
              'width_units': 'mm',
              'height_low': 2.8,
              'height_high': 4.5,
              'height_units': 'mm',
              'trait': 'legume_size',
              'start': 17,
              'end': 41}]
        )

    def test_size_27(self):
        self.assertEqual(
            parse('Racemes 3-4 cm,'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_low': 3,
              'length_high': 4,
              'length_units': 'cm',
              'trait': 'inflorescence_size',
              'start': 8,
              'end': 14}]
        )

    def test_size_28(self):
        self.assertEqual(
            parse('Petals pale violet, with darker keel; standard '
                  'elliptic, 6-7 × 3-4;'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'purple', 'trait': 'petal_color', 'start': 12,
              'end': 18},
             {'subpart': 'keel', 'trait': 'subpart', 'start': 32, 'end': 36},
             {'shape': 'elliptic', 'trait': 'petal_shape', 'start': 47,
              'end': 55}]
        )

    def test_size_29(self):
        self.assertEqual(
            parse('Seeds ca. 1.6 × 1-1.3 × 0.7-0.8 cm; hilum 8-10 mm.'),
            [{'part': 'seed', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 1.6,
              'width_low': 1.0,
              'width_high': 1.3,
              'thickness_low': 0.7,
              'thickness_high': 0.8,
              'thickness_units': 'cm',
              'trait': 'seed_size',
              'start': 6,
              'end': 34},
             {'subpart': 'hilum', 'trait': 'subpart', 'start': 36, 'end': 41},
             {'length_low': 8,
              'length_high': 10,
              'length_units': 'mm',
              'trait': 'seed_hilum_size',
              'start': 42,
              'end': 49}]
        )

    def test_size_30(self):
        self.assertEqual(
            parse('leaflets obovate, 1-2.5 × to 1.6 cm,'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'shape': 'obovate', 'trait': 'leaflet_shape', 'start': 9,
              'end': 16},
             {'length_low': 1.0,
              'length_high': 2.5,
              'width_low': 1.6,
              'width_units': 'cm',
              'trait': 'leaflet_size',
              'start': 18,
              'end': 35}]
        )

    def test_size_31(self):
        self.assertEqual(
            parse('Shrubs, 0.5–1[–2.5] m.'),
            [{'habit': 'shrub', 'trait': 'plant_habit', 'start': 0, 'end': 6},
             {'length_low': 0.5,
              'length_high': 1.0,
              'length_max': 2.5,
              'length_units': 'm',
              'trait': 'plant_size',
              'start': 8,
              'end': 22}]
        )
