"""Test the plant color matcher."""

import unittest

from efloras.matchers.plant_color import PLANT_COLOR
from efloras.pylib.util import DotDict as Trait


class TestPlantColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_plant_color_01(self):
        """It parses compound color notations."""
        self.assertEqual(
            PLANT_COLOR.parse(
                'hypanthium green or greenish yellow, '
                'usually not purple-spotted, rarely purple-spotted distally'),
            [Trait(start=0, end=86, part='hypanthium',
                   value=['green', 'green-yellow', 'purple-spotted'],
                   raw_value='green or greenish yellow, usually not '
                             'purple-spotted, rarely purple-spotted')])

    def test_plant_color_02(self):
        """It parses compound color words."""
        self.assertEqual(
            PLANT_COLOR.parse(
                'hypanthium straw-colored to '
                'sulphur-yellow or golden-yellow'),
            [Trait(start=0, end=59, part='hypanthium',
                   value=['yellow'],
                   raw_value='straw-colored to sulphur-yellow or '
                             'golden-yellow')])

    def test_plant_color_03(self):
        """It normalizes color notations."""
        self.assertEqual(
            PLANT_COLOR.parse(
                'petals 5, connate 1/2-2/3 length, white, cream, '
                'or pale green [orange to yellow], '),
            [Trait(start=0, end=79, part='petals',
                   value=['white', 'green', 'orange', 'yellow'],
                   raw_value='white, cream, or pale green '
                             '[orange to yellow')])

    def test_plant_color_04(self):
        """It handles colors with trailing punctuation."""
        self.assertEqual(
            PLANT_COLOR.parse('sepals erect, green- or red-tipped'),
            [Trait(start=0, end=34, part='sepals',
                   value=['green', 'red-tipped'],
                   raw_value='green- or red-tipped')])

    def test_plant_color_05(self):
        """It handles pattern notations within colors."""
        self.maxDiff = None
        self.assertEqual(
            PLANT_COLOR.parse(
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
            PLANT_COLOR.parse(
                'petals 5, distinct, white to cream, greenish white, '
                'or yellowish green, or yellowish, usually green-throated '
                'and faintly green-lined,'),
            [Trait(start=0, end=132, part='petals',
                   value=['white', 'green-white', 'yellow-green', 'yellow',
                          'green-throated', 'green-lined'],
                   raw_value='white to cream, greenish '
                             'white, or yellowish green, or yellowish, '
                             'usually green-throated and faintly '
                             'green-lined')])
