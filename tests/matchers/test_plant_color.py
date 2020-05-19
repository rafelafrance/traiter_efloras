"""Test the plant color matcher."""

import unittest

from efloras.matchers.matcher import Matcher


class TestPlantColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_plant_color_01(self):
        """It parses compound color notations."""
        self.assertEqual(
            Matcher('*_color').parse(
                'hypanthium green or greenish yellow, '
                'usually not purple-spotted, rarely purple-spotted distally'),
            [{'part': [{'value': 'hypanthium',
                        'start': 0, 'end': 10,
                        'raw_value': 'hypanthium'}],
              'hypanthium_color': [{'value': 'green',
                                    'start': 11, 'end': 16,
                                    'raw_value': 'green'},
                                   {'value': 'green-yellow',
                                    'start': 20, 'end': 35,
                                    'raw_value': 'greenish yellow'},
                                   {'value': 'purple-spotted',
                                    'start': 49, 'end': 63,
                                    'raw_value': 'purple-spotted'},
                                   {'value': 'purple-spotted',
                                    'start': 72, 'end': 86,
                                    'raw_value': 'purple-spotted'}]}])

    def test_plant_color_02(self):
        """It parses compound color words."""
        self.assertEqual(
            Matcher('*_color').parse(
                'hypanthium straw-colored to '
                'sulphur-yellow or golden-yellow'),
            [{'part': [{'value': 'hypanthium',
                        'start': 0, 'end': 10,
                        'raw_value': 'hypanthium'}],
              'hypanthium_color': [{'value': 'yellow',
                                    'start': 11, 'end': 24,
                                    'raw_value': 'straw-colored'},
                                   {'value': 'yellow',
                                    'start': 28, 'end': 42,
                                    'raw_value': 'sulphur-yellow'},
                                   {'value': 'yellow',
                                    'start': 46, 'end': 59,
                                    'raw_value': 'golden-yellow'}]}])

    def test_plant_color_03(self):
        """It normalizes color notations."""
        self.assertEqual(
            Matcher('*_color').parse('sepals erect, green- or red-tipped'),
            [{'part': [{'value': 'sepal', 'start': 0, 'end': 6,
                        'raw_value': 'sepals'}],
              'sepal_color': [{'value': 'green',
                               'start': 14, 'end': 20,
                               'raw_value': 'green-'},
                              {'value': 'red-tipped',
                               'start': 24, 'end': 34,
                               'raw_value': 'red-tipped'}]}]

        )

    def test_plant_color_04(self):
        """It handles colors with trailing punctuation."""
        self.assertEqual(
            Matcher('*_color').parse(
                'petals 5, connate 1/2-2/3 length, white, cream, '
                'or pale green [orange to yellow], '),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 6,
                        'raw_value': 'petals'}],
              'petal_color': [{'value': 'white',
                               'start': 34, 'end': 39,
                               'raw_value': 'white'},
                              {'value': 'white',
                               'start': 41, 'end': 46,
                               'raw_value': 'cream'},
                              {'value': 'green',
                               'start': 56, 'end': 61,
                               'raw_value': 'green'},
                              {'value': 'orange',
                               'start': 63, 'end': 69,
                               'raw_value': 'orange'},
                              {'value': 'yellow',
                               'start': 73, 'end': 79,
                               'raw_value': 'yellow'}]}]

        )

    def test_plant_color_05(self):
        """It handles pattern notations within colors."""
        self.assertEqual(
            Matcher('*_color').parse(
                'petals 5, distinct, white to cream, obovate to '
                'oblong-obovate, (15–)20–greenish yellow, maturing '
                'yellowish or pale brown, commonly mottled or with '
                'light green or white longitudinal stripes'),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 6,
                        'raw_value': 'petals'}],
              'petal_color': [{'value': 'white',
                               'start': 20, 'end': 25,
                               'raw_value': 'white'},
                              {'value': 'white',
                               'start': 29, 'end': 34,
                               'raw_value': 'cream'},
                              {'value': 'green-yellow',
                               'start': 71, 'end': 86,
                               'raw_value': 'greenish yellow'},
                              {'value': 'yellow',
                               'start': 97, 'end': 106,
                               'raw_value': 'yellowish'},
                              {'value': 'brown',
                               'start': 115, 'end': 120,
                               'raw_value': 'brown'},
                              {'value': 'green',
                               'start': 153, 'end': 158,
                               'raw_value': 'green'},
                              {'value': 'white-longitudinal-stripes',
                               'start': 162, 'end': 188,
                               'raw_value': 'white longitudinal stripes'}]}]
        )

    def test_plant_color_06(self):
        """It handles some odd pattern notations like 'throated'."""
        self.assertEqual(
            Matcher('*_color').parse(
                'Petals 5, distinct, white to cream, greenish white, '
                'or yellowish green, or yellowish, usually green-throated '
                'and faintly green-lined,'),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 6,
                        'raw_value': 'Petals'}],
              'petal_color': [{'value': 'white',
                               'start': 20, 'end': 25,
                               'raw_value': 'white'},
                              {'value': 'white',
                               'start': 29, 'end': 34,
                               'raw_value': 'cream'},
                              {'value': 'green-white',
                               'start': 36, 'end': 50,
                               'raw_value': 'greenish white'},
                              {'value': 'yellow-green',
                               'start': 55, 'end': 70,
                               'raw_value': 'yellowish green'},
                              {'value': 'yellow',
                               'start': 75, 'end': 84,
                               'raw_value': 'yellowish'},
                              {'value': 'green-throated',
                               'start': 94, 'end': 108,
                               'raw_value': 'green-throated'},
                              {'value': 'green-lined',
                               'start': 121, 'end': 132,
                               'raw_value': 'green-lined'}]}]
        )

    def test_plant_color_07(self):
        """It parses calyx color."""
        self.maxDiff = None
        self.assertEqual(
            Matcher('calyx_color').parse('calyx yellow'),
            [{'part': [{'value': 'calyx', 'start': 0, 'end': 5,
                        'raw_value': 'calyx'}],
              'calyx_color': [{'value': 'yellow',
                               'start': 6, 'end': 12,
                               'raw_value': 'yellow'}]}]
        )

    def test_plant_color_08(self):
        """It parses corolla color."""
        self.assertEqual(
            Matcher('corolla_color').parse('corolla yellow'),
            [{'part': [{'value': 'corolla', 'start': 0, 'end': 7,
                        'raw_value': 'corolla'}],
              'corolla_color': [{'value': 'yellow',
                                 'start': 8, 'end': 14,
                                 'raw_value': 'yellow'}]}]
        )

    def test_plant_color_09(self):
        """It parses flower color."""
        self.assertEqual(
            Matcher('flower_color').parse('flower yellow'),
            [{'part': [{'value': 'flower', 'start': 0, 'end': 6,
                        'raw_value': 'flower'}],
              'flower_color': [{'value': 'yellow',
                                'start': 7, 'end': 13,
                                'raw_value': 'yellow'}]}]
        )

    def test_plant_color_10(self):
        """It parses hypanthium color."""
        self.maxDiff = None
        self.assertEqual(
            Matcher('hypanthium_color').parse('hypanthium yellow'),
            [{'part': [{'value': 'hypanthium',
                        'start': 0, 'end': 10,
                        'raw_value': 'hypanthium'}],
              'hypanthium_color': [{'value': 'yellow',
                                    'start': 11, 'end': 17,
                                    'raw_value': 'yellow'}]}]
        )

    def test_plant_color_11(self):
        """It parses petal color."""
        self.assertEqual(
            Matcher('petal_color').parse('petal yellow'),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 5,
                        'raw_value': 'petal'}],
              'petal_color': [{'value': 'yellow',
                               'start': 6, 'end': 12,
                               'raw_value': 'yellow'}]}]
        )

    def test_plant_color_12(self):
        """It parses sepal color."""
        self.assertEqual(
            Matcher('sepal_color').parse('sepal yellow'),
            [{'part': [{'value': 'sepal', 'start': 0, 'end': 5,
                        'raw_value': 'sepal'}],
              'sepal_color': [{'value': 'yellow',
                               'start': 6, 'end': 12,
                               'raw_value': 'yellow'}]}]
        )
