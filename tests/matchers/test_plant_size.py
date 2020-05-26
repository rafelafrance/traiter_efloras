"""Test plant size trait matcher."""

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestPlantSize(unittest.TestCase):
    """Test plant size trait parsers."""

    def test_plant_size_01(self):
        self.assertEqual(
            MATCHER.parse('Leaf (12-)23-34 × 45-56 cm'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4}],
              'leaf_size': [{'start': 5, 'end': 26,
                             'value': {'length_min': 120.0,
                                       'length_low': 230.0,
                                       'length_high': 340.0,
                                       'width_low': 450.0,
                                       'width_high': 560.0,
                                       'width_units': 'cm'}}]}]
        )

    def test_plant_size_02(self):
        self.assertEqual(
            MATCHER.parse('leaf (12-)23-34 × 45-56'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4}]}]
        )

    def test_plant_size_03(self):
        self.assertEqual(
            MATCHER.parse('blade 1.5–5(–7) cm'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 5}],
              'leaf_size': [{'start': 6, 'end': 18,
                             'value': {'length_low': 15.0,
                                       'length_high': 50.0,
                                       'length_max': 70.0,
                                       'length_units': 'cm'}}]}]
        )

    def test_plant_size_04(self):
        self.assertEqual(
            MATCHER.parse('leaf shallowly to deeply 5–7-lobed'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4}]}]
        )

    def test_plant_size_05(self):
        self.assertEqual(
            MATCHER.parse('leaf 4–10 cm wide'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4}],
              'leaf_size': [{'start': 5, 'end': 17,
                             'value': {'width_low': 40.0,
                                       'width_high': 100.0,
                                       'width_units': 'cm'}}]}]
        )

    def test_plant_size_06(self):
        self.assertEqual(
            MATCHER.parse('leaf sinuses 1/5–1/4 to base'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4}]},
             {'part': [{'value': 'sinus', 'start': 5, 'end': 12}]}]
        )

    def test_plant_size_07(self):
        self.assertEqual(
            MATCHER.parse('petiolules 2–5 mm'),
            [{'part': [{'value': 'petiole', 'start': 0, 'end': 10}],
              'petiole_size': [{'start': 11, 'end': 17,
                                'value': {'length_low': 2.0,
                                          'length_high': 5.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_08(self):
        self.assertEqual(
            MATCHER.parse(
                'petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm.'),
            [{'part': [{'value': 'petiole', 'start': 0, 'end': 10}],
              'petiole_size': [{'start': 11, 'end': 17,
                                'value': {'length_low': 2.0,
                                          'length_high': 5.0,
                                          'length_units': 'mm'}}]},
             {'part': [{'value': 'petiole', 'start': 37, 'end': 45}],
              'petiole_size': [{'start': 46, 'end': 54,
                                'value': {'length_low': 16.0,
                                          'length_high': 28.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_09(self):
        self.assertEqual(
            MATCHER.parse('Leaves: petiole 2–15 cm;'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6}]},
             {'part': [{'value': 'petiole', 'start': 8, 'end': 15}],
              'petiole_size': [{'start': 16, 'end': 23,
                                'value': {'length_low': 20.0,
                                          'length_high': 150.0,
                                          'length_units': 'cm'}}]}]
        )

    def test_plant_size_10(self):
        self.assertEqual(
            MATCHER.parse(
                'petiole [5–]7–25[–32] mm, glabrous,'),
            [{'part': [{'value': 'petiole', 'start': 0, 'end': 7}],
              'petiole_size': [{'start': 8, 'end': 24,
                                'value': {'length_min': 5.0,
                                          'length_low': 7.0,
                                          'length_high': 25.0,
                                          'length_max': 32.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_11(self):
        self.assertEqual(
            MATCHER.parse('leaf 2–4 cm × 2–10 mm'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4}],
              'leaf_size': [{'start': 5, 'end': 21,
                             'value': {'length_low': 20.0,
                                       'length_high': 40.0,
                                       'length_units': 'cm',
                                       'width_low': 2.0,
                                       'width_high': 10.0,
                                       'width_units': 'mm'}}]}]
        )

    def test_plant_size_12(self):
        self.assertEqual(
            MATCHER.parse(
                'leaf deeply to shallowly lobed, 4–5(–7) cm wide,'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4}],
              'leaf_size': [{'start': 32, 'end': 47,
                             'value': {'width_low': 40.0,
                                       'width_high': 50.0,
                                       'width_max': 70.0,
                                       'width_units': 'cm'}}]}]
        )

    def test_plant_size_13(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves 3-foliolate, lateral pair of leaflets '
                'deeply lobed, petiolules 2–5 mm,'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6}]},
             {'part': [{'value': 'leaf', 'start': 36, 'end': 44}]},
             {'part': [{'value': 'petiole',
                        'start': 59, 'end': 69}],
              'petiole_size': [{'start': 70, 'end': 76,
                                'value': {'length_low': 2.0,
                                          'length_high': 5.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_14(self):
        self.maxDiff = None
        self.assertEqual(
            MATCHER.parse(
                'terminal leaflet 3–5 cm, blade '
                'petiolule 3–12 mm,'),
            [{'part': [{'start': 0, 'end': 16, 'location': 'terminal',
                        'value': 'leaf'}],
              'leaf_size': [{'start': 17, 'end': 23,
                             'value': {'length_low': 30.0,
                                       'length_high': 50.0,
                                       'length_units': 'cm'}}]},
             {'part': [{'start': 25, 'end': 30, 'value': 'leaf'}]},
             {'part': [{'start': 31, 'end': 40, 'value': 'petiole'}],
              'petiole_size': [{'start': 41, 'end': 48,
                                'value': {'length_low': 3.0,
                                          'length_high': 12.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_15(self):
        """It skips lobe counts."""
        self.assertEqual(
            MATCHER.parse('leaf shallowly 3–5(–7)-lobed, '
                          '5–25 × (8–)10–25(–30) cm,'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4}],
              'leaf_size': [{'start': 30, 'end': 54,
                             'value': {'length_low': 50.0,
                                       'length_high': 250.0,
                                       'width_min': 80.0,
                                       'width_low': 100.0,
                                       'width_high': 250.0,
                                       'width_max': 300.0,
                                       'width_units': 'cm'}}]}]
        )

    def test_plant_size_16(self):
        """It handles no plant part."""
        self.assertEqual(
            MATCHER.parse('(3–)5-lobed, 6–20(–30) × 6–25 cm,'),
            []
        )

    def test_plant_size_17(self):
        """It allows an 'up to' type of size notation."""
        self.assertEqual(
            MATCHER.parse('petiole to 11 cm;'),
            [{'part': [{'value': 'petiole', 'start': 0, 'end': 7}],
              'petiole_size': [{'start': 8, 'end': 16,
                                'value': {'length_high': 110.0,
                                          'length_units': 'cm'}}]}]
        )

    def test_plant_size_18(self):
        """It handles sexual dimorphism in size notations."""
        self.assertEqual(
            MATCHER.parse(
                'petals (1–)3–10(–12) mm (pistillate) '
                'or 5–8(–10) mm (staminate)'),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 6}],
              'petal_size': [{'start': 7, 'end': 36,
                              'value': {'length_min': 1.0,
                                        'length_low': 3.0,
                                        'length_high': 10.0,
                                        'length_max': 12.0,
                                        'length_units': 'mm',
                                        'sex': 'pistillate'}},
                             {'start': 40, 'end': 63,
                              'value': {'length_low': 5.0,
                                        'length_high': 8.0,
                                        'length_max': 10.0,
                                        'length_units': 'mm',
                                        'sex': 'staminate'}}]}]
        )

    def test_plant_size_19(self):
        """It handles a diameter as a dimension."""
        self.assertEqual(
            MATCHER.parse(
                'Flowers 5–10 cm diam.; hypanthium 4–8 mm,'),
            [{'part': [{'value': 'flower', 'start': 0, 'end': 7}],
              'flower_size': [{'start': 8,
                               'end': 20,
                               'value': {'diameter_low': 50.0,
                                         'diameter_high': 100.0,
                                         'diameter_units': 'cm'}}]},
             {'part': [{'value': 'hypanthium', 'start': 23, 'end': 33}],
              'hypanthium_size': [{'start': 34, 'end': 40,
                                   'value': {'length_low': 4.0,
                                             'length_high': 8.0,
                                             'length_units': 'mm'}}]}]
        )

    def test_plant_size_20(self):
        self.assertEqual(
            MATCHER.parse(
                'Flowers 5--16 × 4--12 cm'),
            [{'part': [{'value': 'flower', 'start': 0, 'end': 7}],
              'flower_size': [{'start': 8, 'end': 24,
                               'value': {'length_low': 50.0,
                                         'length_high': 160.0,
                                         'width_low': 40.0,
                                         'width_high': 120.0,
                                         'width_units': 'cm'}}]}]
        )

    def test_plant_size_21(self):
        # """It an inflorescence notation."""
        self.assertEqual(
            MATCHER.parse(
                'Inflorescences formed season before flowering and exposed '
                'during winter; staminate catkins in 1 or more clusters '
                'of 2--5, 3--8.5 cm,'),
            [{'part': [{'value': 'inflorescences', 'start': 0, 'end': 14}],
              'inflorescences_count': [
                  {'start': 94, 'end': 95, 'value': {'low': 1}},
                  {'start': 116, 'end': 120,
                   'value': {'low': 2, 'high': 5}}],
              'inflorescences_size': [{'start': 122,
                                       'end': 131,
                                       'value': {'length_low': 30.0,
                                                 'length_high': 85.0,
                                                 'length_units': 'cm'}}]}]
        )

    def test_plant_size_22(self):
        # """It an inflorescence notation."""
        self.assertEqual(
            MATCHER.parse(
                'Leaflets petiolulate; blade ovate, 8-15 × 4-15 cm,'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 8}]},
             {'part': [{'value': 'leaf', 'start': 22, 'end': 27}],
              'leaf_shape': [{'value': 'ovate', 'start': 28, 'end': 33}],
              'leaf_size': [{'start': 35, 'end': 49,
                             'value': {'length_low': 80.0,
                                       'length_high': 150.0,
                                       'width_low': 40.0,
                                       'width_high': 150.0,
                                       'width_units': 'cm'}}]}]
        )
