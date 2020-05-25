"""Test the plant color matcher."""

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestPlantColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_plant_color_01(self):
        self.assertEqual(
            MATCHER.parse(
                'hypanthium green or greenish yellow, '
                'usually not purple-spotted, rarely purple-spotted distally'),
            [{'part': [{'value': 'hypanthium', 'start': 0, 'end': 10}],
              'hypanthium_color': [{'value': 'green', 'start': 11, 'end': 16},
                                   {'value': 'green-yellow', 'start': 20,
                                    'end': 35},
                                   {'value': 'purple-spotted', 'start': 49,
                                    'end': 63},
                                   {'value': 'purple-spotted', 'start': 72,
                                    'end': 86}]}]
        )

    def test_plant_color_02(self):
        self.assertEqual(
            MATCHER.parse(
                'hypanthium straw-colored to '
                'sulphur-yellow or golden-yellow'),
            [{'part': [{'value': 'hypanthium', 'start': 0, 'end': 10}],
              'hypanthium_color': [{'value': 'yellow', 'start': 11, 'end': 24},
                                   {'value': 'yellow', 'start': 28, 'end': 42},
                                   {'value': 'yellow', 'start': 46,
                                    'end': 59}]}]
        )

    def test_plant_color_03(self):
        self.assertEqual(
            MATCHER.parse('sepals erect, green- or red-tipped'),
            [{'part': [{'value': 'sepal', 'start': 0, 'end': 6}],
              'sepal_color': [{'value': 'green', 'start': 14, 'end': 20},
                              {'value': 'red-tipped',
                               'start': 24, 'end': 34}]}]

        )

    def test_plant_color_04(self):
        self.assertEqual(
            MATCHER.parse(
                'petals white, cream, or pale green [orange to yellow], '),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 6}],
              'petal_color': [{'value': 'white', 'start': 7, 'end': 12},
                              {'value': 'white', 'start': 14, 'end': 19},
                              {'value': 'green', 'start': 29, 'end': 34},
                              {'value': 'orange', 'start': 36, 'end': 42},
                              {'value': 'yellow', 'start': 46, 'end': 52}]}]
        )

    def test_plant_color_05(self):
        """It handles pattern notations within colors."""
        self.assertEqual(
            MATCHER.parse(
                'petals distinct, white to cream, greenish yellow, '
                'maturing yellowish or pale brown, commonly mottled or with '
                'light green or white longitudinal stripes'),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 6}],
              'petal_color': [{'value': 'white', 'start': 17, 'end': 22},
                              {'value': 'white', 'start': 26, 'end': 31},
                              {'value': 'green-yellow', 'start': 33,
                               'end': 48},
                              {'value': 'yellow', 'start': 59, 'end': 68},
                              {'value': 'brown', 'start': 77, 'end': 82},
                              {'value': 'green', 'start': 115, 'end': 120},
                              {'value': 'white-longitudinal-stripes',
                               'start': 124, 'end': 150}]}]
        )

    def test_plant_color_06(self):
        self.assertEqual(
            MATCHER.parse(
                'Petals distinct, white to cream, greenish white, '
                'or yellowish green, or yellowish, usually green-throated '
                'and faintly green-lined,'),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 6}],
              'petal_color': [{'value': 'white', 'start': 17, 'end': 22},
                              {'value': 'white', 'start': 26, 'end': 31},
                              {'value': 'green-white', 'start': 33, 'end': 47},
                              {'value': 'yellow-green', 'start': 52,
                               'end': 67},
                              {'value': 'yellow', 'start': 72, 'end': 81},
                              {'value': 'green-throated', 'start': 91,
                               'end': 105},
                              {'value': 'green-lined', 'start': 118,
                               'end': 129}]}]
        )

    def test_plant_color_07(self):
        self.maxDiff = None
        self.assertEqual(
            MATCHER.parse('calyx yellow'),
            [{'part': [{'value': 'calyx', 'start': 0, 'end': 5}],
              'calyx_color': [{'value': 'yellow',
                               'start': 6, 'end': 12}]}]
        )

    def test_plant_color_08(self):
        self.assertEqual(
            MATCHER.parse('corolla yellow'),
            [{'part': [{'value': 'corolla', 'start': 0, 'end': 7}],
              'corolla_color': [{'value': 'yellow', 'start': 8, 'end': 14}]}]
        )

    def test_plant_color_09(self):
        self.assertEqual(
            MATCHER.parse('flower yellow'),
            [{'part': [{'value': 'flower', 'start': 0, 'end': 6}],
              'flower_color': [{'value': 'yellow',  'start': 7, 'end': 13}]}]
        )

    def test_plant_color_10(self):
        self.maxDiff = None
        self.assertEqual(
            MATCHER.parse('hypanthium yellow'),
            [{'part': [{'value': 'hypanthium', 'start': 0, 'end': 10}],
              'hypanthium_color': [{'value': 'yellow',
                                    'start': 11, 'end': 17}]}]
        )

    def test_plant_color_11(self):
        self.assertEqual(
            MATCHER.parse('petal yellow'),
            [{'part': [{'value': 'petal', 'start': 0, 'end': 5}],
              'petal_color': [{'value': 'yellow',
                               'start': 6, 'end': 12}]}]
        )

    def test_plant_color_12(self):
        self.assertEqual(
            MATCHER.parse('sepal yellow'),
            [{'part': [{'value': 'sepal', 'start': 0, 'end': 5}],
              'sepal_color': [{'value': 'yellow', 'start': 6, 'end': 12}]}]
        )
