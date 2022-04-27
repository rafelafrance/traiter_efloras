"""Test the plant descriptor matcher."""
# pylint: disable=missing-function-docstring
import unittest

from tests.setup import test


class TestDescriptor(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_descriptor_01(self):
        self.assertEqual(
            test(
                """
                bisexual (unisexual and plants sometimes gynodioecious,
                or plants dioecious"""
            ),
            [
                {
                    "reproduction": "bisexual",
                    "trait": "reproduction",
                    "start": 0,
                    "end": 8,
                },
                {
                    "reproduction": "unisexual",
                    "trait": "reproduction",
                    "start": 10,
                    "end": 19,
                },
                {"part": "plant", "trait": "part", "start": 24, "end": 30},
                {
                    "reproduction": "gynodioecious",
                    "trait": "reproduction",
                    "start": 41,
                    "end": 54,
                },
                {"part": "plant", "trait": "part", "start": 59, "end": 65},
                {
                    "reproduction": "dioecious",
                    "trait": "reproduction",
                    "start": 66,
                    "end": 75,
                },
            ],
        )

    def test_descriptor_02(self):
        self.maxDiff = None
        self.assertEqual(
            test("Shrubs , to 1.5 m, forming rhizomatous colonies."),
            [
                {"part": "shrub", "trait": "part", "start": 0, "end": 6},
                {
                    "length_high": 1.5,
                    "length_units": "m",
                    "part": "shrub",
                    "trait": "size",
                    "start": 9,
                    "end": 17,
                },
            ],
        )

    def test_descriptor_03(self):
        self.assertEqual(
            test("Stems often caespitose"),
            [
                {"part": "stem", "trait": "part", "start": 0, "end": 5},
                {"habit": "caespitose", "trait": "habit", "start": 12, "end": 22},
            ],
        )

    def test_descriptor_04(self):
        self.assertEqual(
            test("Herbs perennial or subshrubs, epiphytic or epilithic."),
            [
                {"woodiness": "herbaceous", "trait": "woodiness", "start": 0, "end": 5},
                {"duration": "perennial", "trait": "duration", "start": 6, "end": 15},
                {"part": "shrub", "trait": "part", "start": 19, "end": 28},
                {"habitat": "epiphytic", "trait": "habitat", "start": 30, "end": 39},
                {"habitat": "epilithic", "trait": "habitat", "start": 43, "end": 52},
            ],
        )
