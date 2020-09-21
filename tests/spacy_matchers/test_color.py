"""Test the plant color matcher."""

# pylint: disable=missing-function-docstring

import unittest

from src.spacy_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_color_01(self):
        self.assertEqual(
            NLP(
                'hypanthium green or greenish yellow, '
                'usually not purple-spotted, rarely purple-spotted distally'),
            [{'part': 'hypanthium', 'trait': 'part', 'start': 0, 'end': 10},
             {'color': 'green',
              'trait': 'hypanthium_color', 'start': 11, 'end': 16},
             {'color': 'green-yellow',
              'trait': 'hypanthium_color', 'start': 20, 'end': 35},
             {'color': 'purple-spotted',
              'trait': 'hypanthium_color', 'start': 49, 'end': 63},
             {'color': 'purple-spotted',
              'trait': 'hypanthium_color', 'start': 72, 'end': 86}]
        )

    def test_color_02(self):
        self.assertEqual(
            NLP('hypanthium straw-colored to '
                'sulphur-yellow or golden-yellow'),
            [{'part': 'hypanthium', 'trait': 'part', 'start': 0, 'end': 10},
             {'color': 'yellow', 'trait': 'hypanthium_color', 'start': 11,
              'end': 24},
             {'color': 'yellow', 'trait': 'hypanthium_color', 'start': 28,
              'end': 42},
             {'color': 'yellow', 'trait': 'hypanthium_color', 'start': 46,
              'end': 59}]
        )

    def test_color_03(self):
        self.assertEqual(
            NLP('sepals erect, green- or red-tipped'),
            [{'part': 'sepal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'green', 'trait': 'sepal_color', 'start': 14,
              'end': 20},
             {'color': 'red-tipped', 'trait': 'sepal_color', 'start': 24,
              'end': 34}]
        )

    def test_color_04(self):
        self.assertEqual(
            NLP(
                'petals white, cream, or pale green [orange to yellow], '),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'white', 'trait': 'petal_color', 'start': 7, 'end': 12},
             {'color': 'white', 'trait': 'petal_color', 'start': 14,
              'end': 19},
             {'color': 'green', 'trait': 'petal_color', 'start': 29,
              'end': 34},
             {'color': 'orange', 'trait': 'petal_color', 'start': 36,
              'end': 42},
             {'color': 'yellow', 'trait': 'petal_color', 'start': 46,
              'end': 52}]
        )

    def test_color_05(self):
        """It handles pattern notations within colors."""
        self.assertEqual(
            NLP('petals distinct, white to cream, greenish yellow, '
                'maturing yellowish or pale brown, commonly mottled or with '
                'light green or white longitudinal stripes'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'white', 'trait': 'petal_color',
              'start': 17, 'end': 22},
             {'color': 'white', 'trait': 'petal_color',
              'start': 26, 'end': 31},
             {'color': 'green-yellow', 'trait': 'petal_color',
              'start': 33, 'end': 48},
             {'color': 'yellow', 'trait': 'petal_color',
              'start': 59, 'end': 68},
             {'color': 'brown', 'trait': 'petal_color',
              'start': 77, 'end': 82},
             {'color': 'green', 'trait': 'petal_color',
              'start': 115, 'end': 120},
             {'color': 'white-longitudinal-stripes',
              'trait': 'petal_color',
              'start': 124, 'end': 150}]
        )

    def test_color_06(self):
        self.assertEqual(
            NLP('Petals distinct, white to cream, greenish white, '
                'or yellowish green, or yellowish, usually green-throated '
                'and faintly green-lined,'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'white', 'trait': 'petal_color', 'start': 17,
              'end': 22},
             {'color': 'white', 'trait': 'petal_color', 'start': 26,
              'end': 31},
             {'color': 'green-white', 'trait': 'petal_color', 'start': 33,
              'end': 47},
             {'color': 'yellow-green', 'trait': 'petal_color', 'start': 52,
              'end': 67},
             {'color': 'yellow', 'trait': 'petal_color', 'start': 72,
              'end': 81},
             {'color': 'green-throated', 'trait': 'petal_color', 'start': 91,
              'end': 105},
             {'color': 'green-lined', 'trait': 'petal_color', 'start': 118,
              'end': 129}]
        )

    def test_color_07(self):
        self.assertEqual(
            NLP('calyx yellow'),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'color': 'yellow', 'trait': 'calyx_color', 'start': 6,
              'end': 12}]
        )

    def test_color_08(self):
        self.assertEqual(
            NLP('corolla yellow'),
            [{'part': 'corolla', 'trait': 'part', 'start': 0, 'end': 7},
             {'color': 'yellow', 'trait': 'corolla_color', 'start': 8,
              'end': 14}]
        )

    def test_color_09(self):
        self.assertEqual(
            NLP('flower yellow'),
            [{'part': 'flower', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'yellow', 'trait': 'flower_color', 'start': 7,
              'end': 13}]
        )

    def test_color_10(self):
        self.assertEqual(
            NLP('hypanthium yellow'),
            [{'part': 'hypanthium', 'trait': 'part', 'start': 0, 'end': 10},
             {'color': 'yellow', 'trait': 'hypanthium_color', 'start': 11,
              'end': 17}]
        )

    def test_color_11(self):
        self.assertEqual(
            NLP('petal pale sulfur-yellow'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 5},
             {'color': 'yellow', 'trait': 'petal_color', 'start': 11,
              'end': 24}]
        )

    def test_color_12(self):
        self.assertEqual(
            NLP('sepal yellow'),
            [{'part': 'sepal', 'trait': 'part', 'start': 0, 'end': 5},
             {'color': 'yellow', 'trait': 'sepal_color', 'start': 6,
              'end': 12}]
        )

    def test_color_13(self):
        self.assertEqual(
            NLP('Leaves acaulescent or nearly so, with white hairs.'),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 6},
             {'habit': 'acaulescent', 'trait': 'plant_habit', 'start': 7,
              'end': 18},
             {'color': 'white', 'trait': 'leaf_hair_color', 'start': 38,
              'end': 43},
             {'subpart': 'hair', 'trait': 'subpart', 'start': 44, 'end': 49}]
        )

    def test_color_14(self):
        self.assertEqual(
            NLP('leaflets surfaces rather densely spotted with minute '
                'blackish dots,'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'subpart': 'surface', 'trait': 'subpart', 'start': 9, 'end': 17},
             {'color': 'black-dots',
              'trait': 'leaflet_surface_color', 'start': 53, 'end': 66}]
        )

    def test_color_15(self):
        self.assertEqual(
            NLP('Petals purplish in life, whitish yel-lowish when dry;'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'purple', 'trait': 'petal_color', 'start': 7,
              'end': 15},
             {'color': 'white-yellow',
              'trait': 'petal_color', 'start': 25,
              'end': 43}]
        )

    def test_color_16(self):
        self.assertEqual(
            NLP('Petals red or golden yellowish'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'red',
              'trait': 'petal_color', 'start': 7, 'end': 10},
             {'color': 'yellow',
              'trait': 'petal_color', 'start': 14, 'end': 30}]
        )

    def test_color_17(self):
        self.assertEqual(
            NLP('twigs: young growth green or reddish-tinged'),
            [{'part': 'twig', 'trait': 'part', 'start': 0, 'end': 5},
             {'color': 'green',
              'trait': 'twig_color', 'start': 20, 'end': 25},
             {'color': 'red-tinged',
              'trait': 'twig_color', 'start': 29, 'end': 43}]
        )
