"""Test the plant color matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_color_01(self):
        self.assertEqual(
            MATCHER.parse(
                'hypanthium green or greenish yellow, '
                'usually not purple-spotted, rarely purple-spotted distally'),
            {'part': [{'part': 'hypanthium', 'start': 0, 'end': 10}],
             'hypanthium_color': [{'color': 'green', 'start': 11, 'end': 16},
                                  {'color': 'green-yellow', 'start': 20,
                                   'end': 35},
                                  {'color': 'purple-spotted', 'start': 49,
                                   'end': 63},
                                  {'color': 'purple-spotted', 'start': 72,
                                   'end': 86}]}
        )

    def test_color_02(self):
        self.assertEqual(
            MATCHER.parse(
                'hypanthium straw-colored to '
                'sulphur-yellow or golden-yellow'),
            {'part': [{'part': 'hypanthium', 'start': 0, 'end': 10}],
             'hypanthium_color': [{'color': 'yellow', 'start': 11, 'end': 24},
                                  {'color': 'yellow', 'start': 28, 'end': 42},
                                  {'color': 'yellow', 'start': 46, 'end': 59}]}
        )

    def test_color_03(self):
        self.assertEqual(
            MATCHER.parse('sepals erect, green- or red-tipped'),
            {'part': [{'part': 'sepal', 'start': 0, 'end': 6}],
             'sepal_color': [{'color': 'green', 'start': 14, 'end': 20},
                             {'color': 'red-tipped', 'start': 24, 'end': 34}]}
        )

    def test_color_04(self):
        self.assertEqual(
            MATCHER.parse(
                'petals white, cream, or pale green [orange to yellow], '),
            {'part': [{'part': 'petal', 'start': 0, 'end': 6}],
             'petal_color': [{'color': 'white', 'start': 7, 'end': 12},
                             {'color': 'white', 'start': 14, 'end': 19},
                             {'color': 'green', 'start': 29, 'end': 34},
                             {'color': 'orange', 'start': 36, 'end': 42},
                             {'color': 'yellow', 'start': 46, 'end': 52}]}
        )

    def test_color_05(self):
        """It handles pattern notations within colors."""
        self.assertEqual(
            MATCHER.parse(
                'petals distinct, white to cream, greenish yellow, '
                'maturing yellowish or pale brown, commonly mottled or with '
                'light green or white longitudinal stripes'),
            {'part': [{'part': 'petal', 'start': 0, 'end': 6}],
             'petal_color': [{'color': 'white', 'start': 17, 'end': 22},
                             {'color': 'white', 'start': 26, 'end': 31},
                             {'color': 'green-yellow', 'start': 33, 'end': 48},
                             {'color': 'yellow', 'start': 59, 'end': 68},
                             {'color': 'brown', 'start': 77, 'end': 82},
                             {'color': 'green', 'start': 115, 'end': 120},
                             {'color': 'white-longitudinal-stripes',
                              'start': 124, 'end': 150}]}
        )

    def test_color_06(self):
        self.assertEqual(
            MATCHER.parse(
                'Petals distinct, white to cream, greenish white, '
                'or yellowish green, or yellowish, usually green-throated '
                'and faintly green-lined,'),
            {'part': [{'start': 0, 'end': 6, 'part': 'petal'}],
             'petal_color': [{'color': 'white', 'start': 17, 'end': 22},
                             {'color': 'white', 'start': 26, 'end': 31},
                             {'color': 'green-white', 'start': 33, 'end': 47},
                             {'color': 'yellow-green', 'start': 52, 'end': 67},
                             {'color': 'yellow', 'start': 72, 'end': 81},
                             {'color': 'green-throated', 'start': 91,
                              'end': 105},
                             {'color': 'green-lined', 'start': 118,
                              'end': 129}]}
        )

    def test_color_07(self):
        self.assertEqual(
            MATCHER.parse('calyx yellow'),
            {'part': [{'part': 'calyx', 'start': 0, 'end': 5}],
             'calyx_color': [{'color': 'yellow', 'start': 6, 'end': 12}]}
        )

    def test_color_08(self):
        self.assertEqual(
            MATCHER.parse('corolla yellow'),
            {'part': [{'part': 'corolla', 'start': 0, 'end': 7}],
             'corolla_color': [{'color': 'yellow', 'start': 8, 'end': 14}]}
        )

    def test_color_09(self):
        self.assertEqual(
            MATCHER.parse('flower yellow'),
            {'part': [{'part': 'flower', 'start': 0, 'end': 6}],
             'flower_color': [{'color': 'yellow', 'start': 7, 'end': 13}]}
        )

    def test_color_10(self):
        self.assertEqual(
            MATCHER.parse('hypanthium yellow'),
            {'part': [{'part': 'hypanthium', 'start': 0, 'end': 10}],
             'hypanthium_color': [{'color': 'yellow', 'start': 11, 'end': 17}]}
        )

    def test_color_11(self):
        self.assertEqual(
            MATCHER.parse('petal pale sulfur-yellow'),
            {'part': [{'part': 'petal', 'start': 0, 'end': 5}],
             'petal_color': [{'color': 'yellow', 'start': 11, 'end': 24}]}
        )

    def test_color_12(self):
        self.assertEqual(
            MATCHER.parse('sepal yellow'),
            {'part': [{'part': 'sepal', 'start': 0, 'end': 5}],
             'sepal_color': [{'color': 'yellow', 'start': 6, 'end': 12}]}
        )

    def test_color_13(self):
        self.assertEqual(
            MATCHER.parse(
                'Leaves acaulescent or nearly so, with white hairs.'),
            {'part': [{'start': 0, 'end': 6, 'part': 'leaf'}],
             'plant_habit': [{'habit': 'acaulescent', 'start': 7, 'end': 18}],
             'leaf_hair_color': [{'color': 'white', 'start': 38, 'end': 43}],
             'subpart': [{'subpart': 'hair', 'start': 44, 'end': 49}]}
        )

    def test_color_14(self):
        self.assertEqual(
            MATCHER.parse(
                'leaflets surfaces rather densely spotted with minute '
                'blackish dots,'),
            {'part': [{'part': 'leaflet', 'start': 0, 'end': 8}],
             'subpart': [{'subpart': 'surface', 'start': 9, 'end': 17}],
             'leaflet_surface_color': [
                 {'color': 'black-dots', 'start': 53, 'end': 66}]}
        )
