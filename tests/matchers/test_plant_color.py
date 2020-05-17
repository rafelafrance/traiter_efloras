"""Test the plant color matcher."""

import unittest

from traiter.util import DotDict as Trait

from efloras.matchers.base import Base


class TestPlantColor(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_plant_color_01(self):
        """It parses compound color notations."""
        parser = Base()
        self.assertEqual(
            parser.parse(
                'hypanthium green or greenish yellow, '
                'usually not purple-spotted, rarely purple-spotted distally'),
            [Trait(start=11, end=86, part='hypanthium',
                   value=['green', 'green-yellow', 'purple-spotted'],
                   raw_value='green or greenish yellow, usually not '
                             'purple-spotted, rarely purple-spotted')])

    def test_plant_color_02(self):
        """It parses compound color words."""
        parser = Base()
        self.assertEqual(
            parser.parse(
                'hypanthium straw-colored to '
                'sulphur-yellow or golden-yellow'),
            [Trait(start=11, end=59, part='hypanthium',
                   value=['yellow'],
                   raw_value='straw-colored to sulphur-yellow or '
                             'golden-yellow')])

    def test_plant_color_03(self):
        """It normalizes color notations."""
        parser = Base()
        self.assertEqual(
            parser.parse(
                'petals 5, connate 1/2-2/3 length, white, cream, '
                'or pale green [orange to yellow], '),
            [Trait(start=34, end=79, part='petals',
                   value=['white', 'green', 'orange', 'yellow'],
                   raw_value='white, cream, or pale green '
                             '[orange to yellow')])

    def test_plant_color_04(self):
        """It handles colors with trailing punctuation."""
        parser = Base()
        self.assertEqual(
            parser.parse('sepals erect, green- or red-tipped'),
            [Trait(start=14, end=34, part='sepals',
                   value=['green', 'red-tipped'],
                   raw_value='green- or red-tipped')])

    def test_plant_color_05(self):
        """It handles pattern notations within colors."""
        parser = Base()
        self.maxDiff = None
        self.assertEqual(
            parser.parse(
                'petals 5, distinct, white to cream, obovate to '
                'oblong-obovate, (15–)20–greenish yellow, maturing '
                'yellowish or pale brown, commonly mottled or with '
                'light green or white longitudinal stripes'),
            [Trait(start=20, end=188, part='petals',
                   value=['white', 'green-yellow', 'yellow', 'brown', 'green',
                          'white-longitudinal-stripes'],
                   raw_value=(
                       'white to cream, obovate to oblong-obovate, '
                       '(15–)20–greenish yellow, maturing yellowish or '
                       'pale brown, commonly mottled or with light green '
                       'or white longitudinal stripes'))])

    def test_plant_color_06(self):
        """It handles some odd pattern notations like 'throated'."""
        parser = Base()
        self.assertEqual(
            parser.parse(
                'Petals 5, distinct, white to cream, greenish white, '
                'or yellowish green, or yellowish, usually green-throated '
                'and faintly green-lined,'),
            [Trait(start=20, end=132, part='petals',
                   value=['white', 'green-white', 'yellow-green', 'yellow',
                          'green-throated', 'green-lined'],
                   raw_value='white to cream, greenish '
                             'white, or yellowish green, or yellowish, '
                             'usually green-throated and faintly '
                             'green-lined')])

    def test_plant_color_07(self):
        """It parses calyx color."""
        parser = Base('caylx_color')
        self.assertEqual(
            parser.parse('calyx yellow'),
            [Trait(start=6, end=12, part='calyx',
                   value=['yellow'], raw_value='yellow')])

    def test_plant_color_08(self):
        """It parses corolla color."""
        parser = Base('corolla_color')
        self.assertEqual(
            parser.parse('corolla yellow'),
            [Trait(start=8, end=14, part='corolla',
                   value=['yellow'], raw_value='yellow')])

    def test_plant_color_09(self):
        """It parses flower color."""
        parser = Base('flower_color')
        self.assertEqual(
            parser.parse('flower yellow'),
            [Trait(start=7, end=13, part='flower',
                   value=['yellow'], raw_value='yellow')])

    def test_plant_color_10(self):
        """It parses hypanthium color."""
        parser = Base('hypanthium_color')
        self.assertEqual(
            parser.parse('hypanthium yellow'),
            [Trait(start=11, end=17, part='hypanthium',
                   value=['yellow'], raw_value='yellow')])

    def test_plant_color_11(self):
        """It parses petal color."""
        parser = Base('petal_color')
        self.assertEqual(
            parser.parse('petal yellow'),
            [Trait(start=6, end=12, part='petal',
                   value=['yellow'], raw_value='yellow')])

    def test_plant_color_12(self):
        """It parses sepal color."""
        parser = Base('sepal_color')
        self.assertEqual(
            parser.parse('sepal yellow'),
            [Trait(start=6, end=12, part='sepal',
                   value=['yellow'], raw_value='yellow')])
