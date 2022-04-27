"""Test the plant margin shape matcher."""
# pylint: disable=missing-function-docstring
import unittest

from tests.setup import test


class TestMargin(unittest.TestCase):
    """Test the plant margin shape trait parser."""

    def test_margin_01(self):
        self.assertEqual(
            test("margin shallowly undulate-crenate"),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 6},
                {
                    "margin_shape": "undulate-crenate",
                    "trait": "margin_shape",
                    "subpart": "margin",
                    "start": 7,
                    "end": 33,
                },
            ],
        )

    def test_margin_02(self):
        self.maxDiff = None
        self.assertEqual(
            test("margins ciliate, apex acute to long-acuminate,"),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 7},
                {
                    "margin_shape": "ciliate",
                    "trait": "margin_shape",
                    "subpart": "margin",
                    "start": 8,
                    "end": 15,
                },
                {"subpart": "apex", "trait": "subpart", "start": 17, "end": 21},
                {
                    "shape": "acute",
                    "trait": "shape",
                    "subpart": "apex",
                    "start": 22,
                    "end": 27,
                },
                {
                    "shape": "acuminate",
                    "trait": "shape",
                    "subpart": "apex",
                    "start": 31,
                    "end": 45,
                },
            ],
        )

    def test_margin_03(self):
        self.assertEqual(
            test("reniform, undulate-margined"),
            [
                {"shape": "reniform", "trait": "shape", "start": 0, "end": 8},
                {
                    "margin_shape": "undulate",
                    "trait": "margin_shape",
                    "start": 10,
                    "end": 27,
                },
            ],
        )

    def test_margin_04(self):
        self.assertEqual(
            test("margins thickened-corrugated"),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 7},
                {
                    "margin_shape": "corrugated",
                    "trait": "margin_shape",
                    "subpart": "margin",
                    "start": 8,
                    "end": 28,
                },
            ],
        )

    def test_margin_05(self):
        self.assertEqual(
            test(
                """
                margins coarsely toothed or remotely sinuate-dentate
                to serrate,"""
            ),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 7},
                {
                    "margin_shape": "toothed",
                    "trait": "margin_shape",
                    "subpart": "margin",
                    "start": 8,
                    "end": 24,
                },
                {
                    "margin_shape": "sinuate-dentate",
                    "trait": "margin_shape",
                    "subpart": "margin",
                    "start": 28,
                    "end": 52,
                },
                {
                    "margin_shape": "serrate",
                    "trait": "margin_shape",
                    "subpart": "margin",
                    "start": 56,
                    "end": 63,
                },
            ],
        )
