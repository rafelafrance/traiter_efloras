"""Test plant size trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestPlantSize(unittest.TestCase):
    """Test plant size trait parsers."""

    def test_plant_size_01(self):
        self.assertEqual(
            MATCHER.parse('Leaf (12-)23-34 × 45-56 cm'),
            {'part': [{'start': 0, 'end': 4, 'value': 'leaf'}],
             'leaf_size': [{'start': 5, 'end': 26,
                            'length_min': 12.0,
                            'length_low': 23.0,
                            'length_high': 34.0,
                            'width_low': 45.0,
                            'width_high': 56.0,
                            'width_units': 'cm'}]}
        )

    def test_plant_size_02(self):
        self.assertEqual(
            MATCHER.parse('leaf (12-)23-34 × 45-56'),
            {'part': [{'value': 'leaf', 'start': 0, 'end': 4}]}
        )

    def test_plant_size_03(self):
        self.assertEqual(
            MATCHER.parse('blade 1.5–5(–7) cm'),
            {'part': [{'start': 0, 'end': 5, 'value': 'leaf'}],
             'leaf_size': [{'start': 6, 'end': 18,
                            'length_low': 1.5,
                            'length_high': 5.0,
                            'length_max': 7.0,
                            'length_units': 'cm'}]}
        )

    def test_plant_size_04(self):
        self.assertEqual(
            MATCHER.parse('leaf shallowly to deeply 5–7-lobed'),
            {'part': [{'value': 'leaf', 'start': 0, 'end': 4}]}
        )

    def test_plant_size_05(self):
        self.assertEqual(
            MATCHER.parse('leaf 4–10 cm wide'),
            {'part': [{'start': 0, 'end': 4, 'value': 'leaf'}],
             'leaf_size': [{'start': 5, 'end': 17,
                            'width_low': 4.0,
                            'width_high': 10.0,
                            'width_units': 'cm'}]}
        )

    def test_plant_size_06(self):
        self.assertEqual(
            MATCHER.parse('leaf sinuses 1/5–1/4 to base'),
            {'part': [{'start': 0, 'end': 4, 'value': 'leaf'},
                      {'start': 5, 'end': 12, 'value': 'sinus'}]}
        )

    def test_plant_size_07(self):
        self.assertEqual(
            MATCHER.parse('petiolules 2–5 mm'),
            {'part': [{'start': 0, 'end': 10, 'value': 'petiole'}],
             'petiole_size': [{'start': 11, 'end': 17,
                               'length_low': 2.0,
                               'length_high': 5.0,
                               'length_units': 'mm'}]}
        )

    def test_plant_size_08(self):
        self.assertEqual(
            MATCHER.parse(
                'petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm.'),
            {'part': [{'start': 0, 'end': 10, 'value': 'petiole'},
                      {'start': 37, 'end': 45, 'value': 'petiole'}],
             'petiole_size': [{'start': 11, 'end': 17,
                               'length_low': 2.0, 'length_high': 5.0,
                               'length_units': 'mm'},
                              {'start': 46, 'end': 54,
                               'length_low': 16.0, 'length_high': 28.0,
                               'length_units': 'mm'}]}

        )

    def test_plant_size_09(self):
        self.assertEqual(
            MATCHER.parse('Leaves: petiole 2–15 cm;'),
            {'part': [{'start': 0, 'end': 6, 'value': 'leaf'},
                      {'start': 8, 'end': 15, 'value': 'petiole'}],
             'petiole_size': [{'start': 16, 'end': 23,
                               'length_low': 2.0, 'length_high': 15.0,
                               'length_units': 'cm'}]}
        )

    def test_plant_size_10(self):
        self.assertEqual(
            MATCHER.parse(
                'petiole [5–]7–25[–32] mm, glabrous,'),
            {'part': [{'start': 0, 'end': 7, 'value': 'petiole'}],
             'petiole_size': [{'start': 8, 'end': 24,
                               'length_min': 5.0,
                               'length_low': 7.0,
                               'length_high': 25.0,
                               'length_max': 32.0,
                               'length_units': 'mm'}]}
        )

    def test_plant_size_11(self):
        self.assertEqual(
            MATCHER.parse('leaf 2–4 cm × 2–10 mm'),
            {'part': [{'start': 0, 'end': 4, 'value': 'leaf'}],
             'leaf_size': [{'start': 5, 'end': 21,
                            'length_low': 2.0,
                            'length_high': 4.0,
                            'length_units': 'cm',
                            'width_low': 2.0,
                            'width_high': 10.0,
                            'width_units': 'mm'}]}
        )

    def test_plant_size_12(self):
        self.assertEqual(
            MATCHER.parse(
                'leaf deeply to shallowly lobed, 4–5(–7) cm wide,'),
            {'part': [{'start': 0, 'end': 4, 'value': 'leaf'}],
             'leaf_size': [{'start': 32, 'end': 47,
                            'width_low': 4.0,
                            'width_high': 5.0,
                            'width_max': 7.0,
                            'width_units': 'cm'}]}
        )

    def test_plant_size_13(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves 3-foliolate, lateral pair of leaflets '
                'deeply lobed, petiolules 2–5 mm,'),
            {'part': [{'start': 0, 'end': 6, 'value': 'leaf'},
                      {'start': 36, 'end': 44, 'value': 'leaf'},
                      {'start': 59, 'end': 69, 'value': 'petiole'}],
             'petiole_size': [{'start': 70, 'end': 76,
                               'length_low': 2.0, 'length_high': 5.0,
                               'length_units': 'mm'}]}
        )

    def test_plant_size_14(self):
        self.assertEqual(
            MATCHER.parse(
                'terminal leaflet 3–5 cm, blade '
                'petiolule 3–12 mm,'),
            {'part': [{'start': 0, 'end': 16, 'location': 'terminal',
                       'value': 'leaf'},
                      {'location': 'terminal', 'start': 25, 'end': 30,
                       'value': 'leaf'},
                      {'location': 'terminal', 'start': 31, 'end': 40,
                       'value': 'petiole'}],
             'leaf_size': [{'location': 'terminal', 'start': 17, 'end': 23,
                            'length_low': 3.0, 'length_high': 5.0,
                            'length_units': 'cm'}],
             'petiole_size': [{'location': 'terminal', 'start': 41, 'end': 48,
                               'length_low': 3.0, 'length_high': 12.0,
                               'length_units': 'mm'}]}

        )

    def test_plant_size_15(self):
        self.assertEqual(
            MATCHER.parse('leaf shallowly 3–5(–7)-lobed, '
                          '5–25 × (8–)10–25(–30) cm,'),
            {'part': [{'start': 0, 'end': 4, 'value': 'leaf'}],
             'leaf_size': [{'start': 30, 'end': 54,
                            'length_low': 5.0,
                            'length_high': 25.0,
                            'width_min': 8.0,
                            'width_low': 10.0,
                            'width_high': 25.0,
                            'width_max': 30.0,
                            'width_units': 'cm'}]}
        )

    def test_plant_size_16(self):
        self.assertEqual(
            MATCHER.parse('(3–)5-lobed, 6–20(–30) × 6–25 cm,'),
            {'plant_size': [{'start': 13, 'end': 32,
                             'length_low': 6.0,
                             'length_high': 20.0,
                             'length_max': 30.0,
                             'width_low': 6.0,
                             'width_high': 25.0,
                             'width_units': 'cm'}]}
        )

    def test_plant_size_17(self):
        self.assertEqual(
            MATCHER.parse('petiole to 11 cm;'),
            {'part': [{'start': 0, 'end': 7, 'value': 'petiole'}],
             'petiole_size': [{'start': 8, 'end': 16,
                               'length_high': 11.0,
                               'length_units': 'cm'}]}
        )

    def test_plant_size_18(self):
        self.assertEqual(
            MATCHER.parse(
                'petals (1–)3–10(–12) mm (pistillate) '
                'or 5–8(–10) mm (staminate)'),
            {'part': [{'start': 0, 'end': 6, 'value': 'petal'}],
             'petal_size': [{'start': 7, 'end': 36,
                             'length_min': 1.0,
                             'length_low': 3.0,
                             'length_high': 10.0,
                             'length_max': 12.0,
                             'length_units': 'mm',
                             'sex': 'pistillate'},
                            {'start': 40, 'end': 63,
                             'length_low': 5.0,
                             'length_high': 8.0,
                             'length_max': 10.0,
                             'length_units': 'mm',
                             'sex': 'staminate'}]}
        )

    def test_plant_size_19(self):
        self.assertEqual(
            MATCHER.parse(
                'Flowers 5–10 cm diam.; hypanthium 4–8 mm,'),
            {'part': [{'start': 0, 'end': 7, 'value': 'flower'},
                      {'start': 23, 'end': 33, 'value': 'hypanthium'}],
             'flower_size': [{'start': 8, 'end': 20,
                              'diameter_low': 5.0,
                              'diameter_high': 10.0,
                              'diameter_units': 'cm'}],
             'hypanthium_size': [{'start': 34, 'end': 40,
                                  'length_low': 4.0,
                                  'length_high': 8.0,
                                  'length_units': 'mm'}]}
        )

    def test_plant_size_20(self):
        self.assertEqual(
            MATCHER.parse(
                'Flowers 5--16 × 4--12 cm'),
            {'part': [{'start': 0, 'end': 7, 'value': 'flower'}],
             'flower_size': [{'start': 8, 'end': 24,
                              'length_low': 5.0, 'length_high': 16.0,
                              'width_low': 4.0, 'width_high': 12.0,
                              'width_units': 'cm'}]}
        )

    def test_plant_size_21(self):
        self.assertEqual(
            MATCHER.parse(
                'Inflorescences formed season before flowering and exposed '
                'during winter; staminate catkins in 1 or more clusters '
                'of 2--5, 3--8.5 cm,'),
            {'part': [{'start': 0, 'end': 14, 'value': 'inflorescences'}],
             'inflorescences_count': [{'start': 94, 'end': 95, 'low': 1},
                                      {'start': 116, 'end': 120, 'low': 2,
                                       'high': 5}],
             'inflorescences_size': [{'start': 122,
                                      'end': 131,
                                      'length_low': 3.0,
                                      'length_high': 8.5,
                                      'length_units': 'cm'}]}
        )

    def test_plant_size_22(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaflets petiolulate; blade ovate, 8-15 × 4-15 cm,'),
            {'part': [{'start': 0, 'end': 8, 'value': 'leaf'},
                      {'start': 22, 'end': 27, 'value': 'leaf'}],
             'leaf_shape': [{'value': 'ovate', 'start': 28, 'end': 33}],
             'leaf_size': [{'start': 35, 'end': 49,
                            'length_low': 8.0, 'length_high': 15.0,
                            'width_low': 4.0, 'width_high': 15.0,
                            'width_units': 'cm'}]}
        )

    def test_plant_size_23(self):
        self.assertEqual(
            MATCHER.parse('calyx, 8-10 mm, 3-4 mm high,'),
            {'part': [{'start': 0, 'end': 5, 'value': 'calyx'}],
             'calyx_size': [{'start': 7, 'end': 14,
                             'length_low': 8.0,
                             'length_high': 10.0,
                             'length_units': 'mm'},
                            {'start': 16, 'end': 27,
                             'height_low': 3.0,
                             'height_high': 4.0,
                             'height_units': 'mm'}]}
        )
