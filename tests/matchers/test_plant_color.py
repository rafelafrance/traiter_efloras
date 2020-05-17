"""Test the plant color matcher."""

import unittest

from efloras.matchers.base import Base
from efloras.pylib.util import DotDict as Trait

PARSER = Base()


class TestPlantColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_plant_color_01(self):
        """It parses compound color notations."""
        self.assertEqual(
            PARSER.parse(
                'hypanthium green or greenish yellow, '
                'usually not purple-spotted, rarely purple-spotted distally'),
            [Trait(start=0, end=86, part='hypanthium',
                   value=['green', 'green-yellow', 'purple-spotted'],
                   raw_value='green or greenish yellow, usually not '
                             'purple-spotted, rarely purple-spotted')])

    def test_plant_color_02(self):
        """It parses compound color words."""
        self.assertEqual(
            PARSER.parse(
                'hypanthium straw-colored to '
                'sulphur-yellow or golden-yellow'),
            [Trait(start=0, end=59, part='hypanthium',
                   value=['yellow'],
                   raw_value='straw-colored to sulphur-yellow or '
                             'golden-yellow')])

    def test_plant_color_03(self):
        """It normalizes color notations."""
        self.assertEqual(
            PARSER.parse(
                'petals 5, connate 1/2-2/3 length, white, cream, '
                'or pale green [orange to yellow], '),
            [Trait(start=0, end=79, part='petals',
                   value=['white', 'green', 'orange', 'yellow'],
                   raw_value='white, cream, or pale green '
                             '[orange to yellow')])

    def test_plant_color_04(self):
        """It handles colors with trailing punctuation."""
        self.assertEqual(
            PARSER.parse('sepals erect, green- or red-tipped'),
            [Trait(start=0, end=34, part='sepals',
                   value=['green', 'red-tipped'],
                   raw_value='green- or red-tipped')])

    def test_plant_color_05(self):
        """It handles pattern notations within colors."""
        self.maxDiff = None
        self.assertEqual(
            PARSER.parse(
                'petals 5, distinct, white to cream, obovate to '
                'oblong-obovate, (15–)20–greenish yellow, maturing '
                'yellowish or pale brown, commonly mottled or with '
                'light green or white longitudinal stripes'),
            [Trait(start=0, end=188, part='petals',
                   value=['white', 'green-yellow', 'yellow', 'brown', 'green',
                          'white-longitudinal-stripes'],
                   raw_value=(
                       'white to cream, obovate to oblong-obovate, '
                       '(15–)20–greenish yellow, maturing yellowish or '
                       'pale brown, commonly mottled or with light green '
                       'or white longitudinal stripes'))])

    def test_plant_color_06(self):
        """It handles some odd pattern notations like 'throated'."""
        self.assertEqual(
            PARSER.parse(
                'Petals 5, distinct, white to cream, greenish white, '
                'or yellowish green, or yellowish, usually green-throated '
                'and faintly green-lined,'),
            [Trait(start=0, end=132, part='petals',
                   value=['white', 'green-white', 'yellow-green', 'yellow',
                          'green-throated', 'green-lined'],
                   raw_value='white to cream, greenish '
                             'white, or yellowish green, or yellowish, '
                             'usually green-throated and faintly '
                             'green-lined')])

    def test_plant_color_07(self):
        """It parses compound color notations."""
        self.assertEqual(
            PARSER.parse(
                'hypanthium purple-spotted'),
            [Trait(start=0, end=26, part='hypanthium',
                   value=['purple-spotted'], raw_value='purple-spotted')])

    # def test_plant_color_07(self):
    #     """It parses calyx color."""
    #     self.assertEqual(
    #         CAYLX_COLOR.parse('calyx yellow'),
    #         [Trait(start=0, end=12, part='calyx',
    #                value=['yellow'], raw_value='yellow')])
    #
    # def test_plant_color_08(self):
    #     """It parses corolla color."""
    #     self.assertEqual(
    #         COROLLA_COLOR.parse('corolla yellow'),
    #         [Trait(start=0, end=14, part='corolla',
    #                value=['yellow'], raw_value='yellow')])
    #
    # def test_plant_color_09(self):
    #     """It parses flower color."""
    #     self.assertEqual(
    #         FLOWER_COLOR.parse('flower yellow'),
    #         [Trait(start=0, end=13, part='flower',
    #                value=['yellow'], raw_value='yellow')])
    #
    # def test_plant_color_10(self):
    #     """It parses hypanthium color."""
    #     self.assertEqual(
    #         HYPANTHIUM_COLOR.parse('hypanthium yellow'),
    #         [Trait(start=0, end=17, part='hypanthium',
    #                value=['yellow'], raw_value='yellow')])
    #
    # def test_plant_color_11(self):
    #     """It parses petal color."""
    #     self.assertEqual(
    #         PETAL_COLOR.parse('petal yellow'),
    #         [Trait(start=0, end=12, part='petal',
    #                value=['yellow'], raw_value='yellow')])
    #
    # def test_plant_color_12(self):
    #     """It parses sepal color."""
    #     self.assertEqual(
    #         SEPAL_COLOR.parse('sepal yellow'),
    #         [Trait(start=0, end=12, part='sepal',
    #                value=['yellow'], raw_value='yellow')])
