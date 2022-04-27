"""Test matching literal phrases."""
# pylint: disable=missing-function-docstring
import unittest

from tests.setup import test


class TestPart(unittest.TestCase):
    """Test the plant part parser."""

    def test_part_01(self):
        self.assertEqual(
            test("with thick, woody rootstock."),
            [
                {
                    "woodiness": "woody",
                    "trait": "woodiness",
                    "part": "rootstock",
                    "start": 12,
                    "end": 17,
                },
                {"part": "rootstock", "trait": "part", "start": 18, "end": 27},
            ],
        )

    def test_part_02(self):
        self.assertEqual(
            test("leaflets mostly 1 or 3"),
            [
                {"part": "leaflet", "trait": "part", "start": 0, "end": 8},
                {
                    "low": 1,
                    "high": 3,
                    "trait": "count",
                    "part": "leaflet",
                    "start": 16,
                    "end": 22,
                },
            ],
        )

    def test_part_03(self):
        self.assertEqual(test("Receptacle discoid."), [])

    def test_part_04(self):
        self.assertEqual(
            test("Flowers: sepals (pistillate)"),
            [
                {
                    "part": "flower",
                    "sex": "pistillate",
                    "trait": "part",
                    "start": 0,
                    "end": 7,
                },
                {
                    "part": "sepal",
                    "trait": "part",
                    "start": 9,
                    "end": 15,
                    "sex": "pistillate",
                },
                {
                    "sex": "pistillate",
                    "trait": "sex",
                    "start": 16,
                    "end": 28,
                    "part": "sepal",
                },
            ],
        )

    def test_part_05(self):
        self.assertEqual(
            test("Flowers: staminate:"),
            [
                {
                    "part": "flower",
                    "trait": "part",
                    "start": 0,
                    "end": 7,
                    "sex": "staminate",
                },
                {
                    "sex": "staminate",
                    "trait": "sex",
                    "start": 9,
                    "end": 18,
                    "part": "flower",
                },
            ],
        )
