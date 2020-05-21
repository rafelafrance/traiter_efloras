"""Test plant size trait matcher."""

import unittest

from efloras.matchers.matcher import Matcher


class TestPlantSize(unittest.TestCase):
    """Test plant size trait parsers."""

    def test_plant_size_01(self):
        """It parses a cross measurement."""
        self.assertEqual(
            Matcher('*_size').parse('Leaf (12-)23-34 × 45-56 cm'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 4, 'raw_value': 'Leaf'}],
                'leaf_size': [{'start': 5,
                               'end': 26,
                               'raw_value': '(12-)23-34 × 45-56 cm',
                               'value': {'length_min': 120.0,
                                         'length_low': 230.0,
                                         'length_high': 340.0,
                                         'width_low': 450.0,
                                         'width_high': 560.0,
                                         'width_units': 'cm'}}]}]
        )

    def test_plant_size_02(self):
        """Units are required."""
        self.assertEqual(
            Matcher('*_size').parse('leaf (12-)23-34 × 45-56'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4,
                        'raw_value': 'leaf'}]}]
        )

    def test_plant_size_03(self):
        """It parses a range simple measurement."""
        self.assertEqual(
            Matcher('*_size').parse('blade 1.5–5(–7) cm'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 5, 'raw_value': 'blade'}],
                'leaf_size': [{'start': 6,
                               'end': 18,
                               'raw_value': '1.5–5(–7) cm',
                               'value': {'length_low': 15.0,
                                         'length_high': 50.0,
                                         'length_max': 70.0,
                                         'length_units': 'cm'}}]}]
        )

    def test_plant_size_04(self):
        """It does not allow trailing dashes."""
        self.assertEqual(
            Matcher('*_size').parse('leaf shallowly to deeply 5–7-lobed'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4,
                        'raw_value': 'leaf'}]}]
        )

    def test_plant_size_05(self):
        """It get a dimension."""
        self.assertEqual(
            Matcher('*_size').parse('leaf 4–10 cm wide'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 4, 'raw_value': 'leaf'}],
                'leaf_size': [{'start': 5,
                               'end': 17,
                               'raw_value': '4–10 cm wide',
                               'value': {'width_low': 40.0,
                                         'width_high': 100.0,
                                         'width_units': 'cm'}}]}]
        )

    def test_plant_size_06(self):
        """It does not interpret fractions as a range."""
        self.assertEqual(
            Matcher('*_size').parse('leaf sinuses 1/5–1/4 to base'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 4,
                        'raw_value': 'leaf'}]}]
        )

    def test_plant_size_07(self):
        """It allows a simple range."""
        self.assertEqual(
            Matcher('*_size').parse('petiolules 2–5 mm'),
            [{'part': [{'value': 'petiole',
                        'start': 0,
                        'end': 10,
                        'raw_value': 'petiolules'}],
              'petiole_size': [{'start': 11,
                                'end': 17,
                                'raw_value': '2–5 mm',
                                'value': {'length_low': 2.0,
                                          'length_high': 5.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_08(self):
        """It picks up multiple measurements."""
        self.assertEqual(
            Matcher('*_size').parse(
                'petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm.'),
            [{'part': [{'value': 'petiole',
                        'start': 0,
                        'end': 10,
                        'raw_value': 'petiolules'}],
              'petiole_size': [{'start': 11,
                                'end': 17,
                                'raw_value': '2–5 mm',
                                'value': {'length_low': 2.0,
                                          'length_high': 5.0,
                                          'length_units': 'mm'}}]},
             {'part': [{'value': 'petiole',
                        'start': 37,
                        'end': 45,
                        'raw_value': 'petioles'}],
              'petiole_size': [{'start': 46,
                                'end': 54,
                                'raw_value': '16–28 mm',
                                'value': {'length_low': 16.0,
                                          'length_high': 28.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_09(self):
        """It allows a simple range."""
        self.assertEqual(
            Matcher('*_size').parse('Leaves: petiole 2–15 cm;'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6,
                        'raw_value': 'Leaves'}]},
             {'part': [{'value': 'petiole', 'start': 8, 'end': 15,
                        'raw_value': 'petiole'}],
              'petiole_size': [{'start': 16,
                                'end': 23,
                                'raw_value': '2–15 cm',
                                'value': {'length_low': 20.0,
                                          'length_high': 150.0,
                                          'length_units': 'cm'}}]}]
        )

    def test_plant_size_10(self):
        """It allows alternate opening and closing brackets."""
        self.assertEqual(
            Matcher('*_size').parse(
                'oblong [suborbiculate], petiole [5–]7–25[–32] mm, glabrous,'),
            [{'part': [{'value': 'petiole',
                        'start': 24,
                        'end': 31,
                        'raw_value': 'petiole'}],
              'petiole_size': [{'start': 32,
                                'end': 48,
                                'raw_value': '[5–]7–25[–32] mm',
                                'value': {'length_min': 5.0,
                                          'length_low': 7.0,
                                          'length_high': 25.0,
                                          'length_max': 32.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_11(self):
        """It handles different units for width and length."""
        self.assertEqual(
            Matcher('*_size').parse('leaf 2–4 cm × 2–10 mm'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 4, 'raw_value': 'leaf'}],
                'leaf_size': [{'start': 5,
                               'end': 21,
                               'raw_value': '2–4 cm × 2–10 mm',
                               'value': {'length_low': 20.0,
                                         'length_high': 40.0,
                                         'length_units': 'cm',
                                         'width_low': 2.0,
                                         'width_high': 10.0,
                                         'width_units': 'mm'}}]}]
        )

    def test_plant_size_12(self):
        """It get a measurement separated by a count."""
        self.assertEqual(
            Matcher('*_size').parse(
                'leaf deeply to shallowly lobed, 4–5(–7) cm wide,'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 4, 'raw_value': 'leaf'}],
                'leaf_size': [{'start': 32,
                               'end': 47,
                               'raw_value': '4–5(–7) cm wide',
                               'value': {'width_low': 40.0,
                                         'width_high': 50.0,
                                         'width_max': 70.0,
                                         'width_units': 'cm'}}]}]
        )

    def test_plant_size_13(self):
        """It handles a range after a lobe notation."""
        self.assertEqual(
            Matcher('*_size').parse(
                'Leaves 3-foliolate, lateral pair of leaflets '
                'deeply lobed, petiolules 2–5 mm,'),
            [{'part': [{'value': 'leaf', 'start': 0, 'end': 6,
                        'raw_value': 'Leaves'}]},
             {'part': [{'value': 'leaf', 'start': 36, 'end': 44,
                        'raw_value': 'leaflets'}]},
             {'part': [{'value': 'petiole',
                        'start': 59,
                        'end': 69,
                        'raw_value': 'petiolules'}],
              'petiole_size': [{'start': 70,
                                'end': 76,
                                'raw_value': '2–5 mm',
                                'value': {'length_low': 2.0,
                                          'length_high': 5.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_14(self):
        """It gets a location with the size."""
        self.maxDiff = None
        self.assertEqual(
            Matcher('*_size').parse(
                'terminal leaflet 3–5 cm, blade '
                'narrowly lanceolate, petiolule 3–12 mm,'),
            [{'part': [{'value': 'leaf', 'start': 9, 'end': 16,
                        'raw_value': 'leaflet'}],
              'leaf_size': [{'start': 17,
                             'end': 23,
                             'raw_value': '3–5 cm',
                             'value': {'length_low': 30.0,
                                       'length_high': 50.0,
                                       'length_units': 'cm'}}]},
             {'part': [{'value': 'leaf', 'start': 25, 'end': 30,
                        'raw_value': 'blade'}]},
             {'part': [{'value': 'petiole',
                        'start': 52,
                        'end': 61,
                        'raw_value': 'petiolule'}],
              'petiole_size': [{'start': 62,
                                'end': 69,
                                'raw_value': '3–12 mm',
                                'value': {'length_low': 3.0,
                                          'length_high': 12.0,
                                          'length_units': 'mm'}}]}]
        )

    def test_plant_size_15(self):
        """It skips lobe counts."""
        self.assertEqual(
            Matcher('*_size').parse('leaf shallowly 3–5(–7)-lobed, '
                                    '5–25 × (8–)10–25(–30) cm,'),
            [{'part': [
                {'value': 'leaf', 'start': 0, 'end': 4, 'raw_value': 'leaf'}],
                'leaf_size': [{'start': 30,
                               'end': 54,
                               'raw_value': '5–25 × (8–)10–25(–30) cm',
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
            Matcher('*_size').parse('(3–)5-lobed, 6–20(–30) × 6–25 cm,'),
            []
        )

    def test_plant_size_17(self):
        """It allows an 'up to' type of size notation."""
        self.assertEqual(
            Matcher('*_size').parse('petiole to 11 cm;'),
            [{'part': [{'value': 'petiole', 'start': 0, 'end': 7,
                        'raw_value': 'petiole'}],
              'petiole_size': [{'start': 8,
                                'end': 16,
                                'raw_value': 'to 11 cm',
                                'value': {'length_high': 110.0,
                                          'length_units': 'cm'}}]}]
        )

    def test_plant_size_18(self):
        """It handles sexual dimorphism in size notations."""
        self.assertEqual(
            Matcher('*_size').parse(
                'petals (1–)3–10(–12) mm (pistillate) '
                'or 5–8(–10) mm (staminate)'),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 6,
                        'raw_value': 'petals'}],
              'petal_size': [{'start': 7,
                              'end': 36,
                              'raw_value': '(1–)3–10(–12) mm (pistillate)',
                              'value': {'length_min': 1.0,
                                        'length_low': 3.0,
                                        'length_high': 10.0,
                                        'length_max': 12.0,
                                        'length_units': 'mm',
                                        'sex': 'pistillate'}},
                             {'start': 40,
                              'end': 63,
                              'raw_value': '5–8(–10) mm (staminate)',
                              'value': {'length_low': 5.0,
                                        'length_high': 8.0,
                                        'length_max': 10.0,
                                        'length_units': 'mm',
                                        'sex': 'staminate'}}]}]
        )

    def test_plant_size_19(self):
        """It handles a diameter as a dimension."""
        self.assertEqual(
            Matcher('*_size').parse(
                'Flowers 5–10 cm diam.; hypanthium 4–8 mm,'),
            [{'part': [{'value': 'flower', 'start': 0, 'end': 7,
                        'raw_value': 'Flowers'}],
              'flower_size': [{'start': 8,
                               'end': 20,
                               'raw_value': '5–10 cm diam',
                               'value': {'diameter_low': 50.0,
                                         'diameter_high': 100.0,
                                         'diameter_units': 'cm'}}]},
             {'part': [{'value': 'hypanthium',
                        'start': 23,
                        'end': 33,
                        'raw_value': 'hypanthium'}],
              'hypanthium_size': [{'start': 34,
                                   'end': 40,
                                   'raw_value': '4–8 mm',
                                   'value': {'length_low': 4.0,
                                             'length_high': 8.0,
                                             'length_units': 'mm'}}]}]
        )

    def test_plant_size_20(self):
        """It handles a double dash notation."""
        self.assertEqual(
            Matcher('*_size').parse(
                'Flowers 5--16 × 4--12 cm'),
            [{'part': [{'value': 'flower', 'start': 0, 'end': 7,
                        'raw_value': 'Flowers'}],
              'flower_size': [{'start': 8,
                               'end': 24,
                               'raw_value': '5--16 × 4--12 cm',
                               'value': {'length_low': 50.0,
                                         'length_high': 160.0,
                                         'width_low': 40.0,
                                         'width_high': 120.0,
                                         'width_units': 'cm'}}]}]
        )
