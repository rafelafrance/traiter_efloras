"""Test plant count trait matcher."""
import unittest

from tests.setup import test


class TestCount(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_count_01(self):
        self.assertEqual(
            test("Seeds [1–]3–12[–30]."),
            [
                {"part": "seed", "trait": "part", "start": 0, "end": 5},
                {
                    "min": 1,
                    "low": 3,
                    "high": 12,
                    "max": 30,
                    "trait": "count",
                    "part": "seed",
                    "start": 6,
                    "end": 19,
                },
            ],
        )

    def test_count_02(self):
        """It parses a seed count."""
        self.assertEqual(
            test("Seeds 3–12."),
            [
                {"part": "seed", "trait": "part", "start": 0, "end": 5},
                {
                    "low": 3,
                    "high": 12,
                    "trait": "count",
                    "part": "seed",
                    "start": 6,
                    "end": 10,
                },
            ],
        )

    def test_count_03(self):
        self.assertEqual(
            test("blade 5–10 × 4–9 cm"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 5},
                {
                    "length_low": 5.0,
                    "length_high": 10.0,
                    "length_units": "cm",
                    "width_low": 4.0,
                    "width_high": 9.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 6,
                    "end": 19,
                    "part": "leaf",
                },
            ],
        )

    def test_count_04(self):
        self.assertEqual(
            test("petals 5, connate 1/2–2/3 length"),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {"low": 5, "trait": "count", "part": "petal", "start": 7, "end": 8},
                {
                    "shape": "connate",
                    "trait": "shape",
                    "part": "petal",
                    "start": 10,
                    "end": 17,
                },
            ],
        )

    def test_count_05(self):
        self.assertEqual(
            test("ovules mostly 120–200."),
            [
                {"part": "ovary", "trait": "part", "start": 0, "end": 6},
                {
                    "low": 120,
                    "high": 200,
                    "trait": "count",
                    "part": "ovary",
                    "start": 14,
                    "end": 21,
                },
            ],
        )

    def test_count_06(self):
        self.assertEqual(
            test("Staminate flowers (3–)5–10(–20)"),
            [
                {
                    "sex": "staminate",
                    "part": "flower",
                    "trait": "sex",
                    "start": 0,
                    "end": 9,
                },
                {
                    "part": "flower",
                    "trait": "part",
                    "start": 10,
                    "end": 17,
                    "sex": "staminate",
                },
                {
                    "min": 3,
                    "low": 5,
                    "high": 10,
                    "max": 20,
                    "trait": "count",
                    "start": 18,
                    "end": 31,
                    "part": "flower",
                    "sex": "staminate",
                },
            ],
        )

    def test_count_07(self):
        self.assertEqual(
            test("Ovaries (4 or)5,"),
            [
                {"part": "ovary", "trait": "part", "start": 0, "end": 7},
                {
                    "min": 4,
                    "low": 5,
                    "trait": "count",
                    "part": "ovary",
                    "start": 8,
                    "end": 15,
                },
            ],
        )

    def test_count_08(self):
        self.assertEqual(
            test("Seeds 5(or 6)"),
            [
                {"part": "seed", "trait": "part", "start": 0, "end": 5},
                {
                    "low": 5,
                    "max": 6,
                    "trait": "count",
                    "part": "seed",
                    "start": 6,
                    "end": 13,
                },
            ],
        )

    def test_count_09(self):
        self.assertEqual(
            test("Seeds 5 (or 6)"),
            [
                {"part": "seed", "trait": "part", "start": 0, "end": 5},
                {
                    "low": 5,
                    "max": 6,
                    "trait": "count",
                    "part": "seed",
                    "start": 6,
                    "end": 14,
                },
            ],
        )

    def test_count_10(self):
        self.assertEqual(
            test("leaf (12-)23-34 × 45-56"),
            [{"part": "leaf", "trait": "part", "start": 0, "end": 4}],
        )

    def test_count_11(self):
        self.assertEqual(
            test("stigma papillose on 1 side,"),
            [{"part": "stigma", "trait": "part", "start": 0, "end": 6}],
        )

    def test_count_12(self):
        self.assertEqual(
            test("Male flowers with 2-8(-20) stamens;"),
            [
                {"sex": "male", "trait": "sex", "start": 0, "end": 4, "part": "flower"},
                {
                    "part": "flower",
                    "trait": "part",
                    "start": 5,
                    "end": 12,
                    "sex": "male",
                },
                {
                    "low": 2,
                    "high": 8,
                    "max": 20,
                    "trait": "count",
                    "start": 18,
                    "end": 26,
                    "part": "stamen",
                    "sex": "male",
                },
                {
                    "part": "stamen",
                    "trait": "part",
                    "start": 27,
                    "end": 34,
                    "sex": "male",
                },
            ],
        )

    def test_count_13(self):
        self.maxDiff = None
        self.assertEqual(
            test("leaflets in 3 or 4 pairs,"),
            [
                {"part": "leaflet", "trait": "part", "start": 0, "end": 8},
                {
                    "low": 3,
                    "high": 4,
                    "count_group": "pairs",
                    "trait": "count",
                    "start": 12,
                    "end": 24,
                    "part": "leaflet",
                },
            ],
        )

    def test_count_14(self):
        self.assertEqual(
            test("leaflets/lobes 11–23,"),
            [
                {"part": "leaflet", "trait": "part", "start": 0, "end": 8},
                {
                    "subpart": "lobe",
                    "part": "leaflet",
                    "trait": "subpart",
                    "start": 9,
                    "end": 14,
                },
                {
                    "low": 11,
                    "high": 23,
                    "trait": "count",
                    "part": "leaflet",
                    "subpart": "lobe",
                    "start": 15,
                    "end": 20,
                },
            ],
        )

    def test_count_15(self):
        self.assertEqual(
            test("leaflets in 3 or 4(or 5) pairs,"),
            [
                {"part": "leaflet", "trait": "part", "start": 0, "end": 8},
                {
                    "low": 3,
                    "high": 4,
                    "max": 5,
                    "count_group": "pairs",
                    "trait": "count",
                    "start": 12,
                    "end": 30,
                    "part": "leaflet",
                },
            ],
        )

    def test_count_16(self):
        self.assertEqual(
            test("plants weigh up to 200 pounds"),
            [{"part": "plant", "trait": "part", "start": 0, "end": 6}],
        )

    def test_count_17(self):
        self.maxDiff = None
        self.assertEqual(
            test(
                """
                Pistillate flowers: hyaline bristle at apex of hypanthial
                aculei 0.5–1 times as long as opaque base."""
            ),
            [
                {
                    "sex": "pistillate",
                    "trait": "sex",
                    "start": 0,
                    "end": 10,
                    "part": "flower",
                    "subpart": "setae",
                },
                {
                    "part": "flower",
                    "trait": "part",
                    "start": 11,
                    "end": 18,
                    "sex": "pistillate",
                },
                {
                    "subpart": "setae",
                    "trait": "subpart",
                    "start": 28,
                    "end": 35,
                    "part": "flower",
                    "sex": "pistillate",
                },
                {
                    "subpart_location": "at apex of hypanthial aculei",
                    "trait": "part_as_loc",
                    "start": 36,
                    "end": 64,
                    "part": "flower",
                    "sex": "pistillate",
                    "subpart": "setae",
                },
                {
                    "subpart": "base",
                    "trait": "subpart",
                    "start": 95,
                    "end": 99,
                    "part": "flower",
                    "sex": "pistillate",
                },
            ],
        )

    def test_count_18(self):
        self.assertEqual(
            test("rarely 1- or 5-7-foliolate;"),
            [
                {
                    "min": 1,
                    "low": 5,
                    "max": 7,
                    "trait": "count",
                    "start": 7,
                    "end": 16,
                    "subpart": "lobe",
                },
                {"subpart": "lobe", "trait": "subpart", "start": 16, "end": 26},
            ],
        )

    def test_count_19(self):
        self.assertEqual(
            test("Leaves imparipinnate, 5- or 7(or 9)-foliolate;"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 6},
                {
                    "low": 5,
                    "high": 7,
                    "max": 9,
                    "trait": "count",
                    "start": 22,
                    "end": 35,
                    "part": "leaf",
                },
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 35,
                    "end": 45,
                    "part": "leaf",
                },
            ],
        )

    def test_count_20(self):
        self.assertEqual(
            test("Seeds (1 or)2 or 3 per legume,"),
            [
                {"part": "seed", "trait": "part", "start": 0, "end": 5},
                {
                    "min": 1,
                    "low": 2,
                    "high": 3,
                    "trait": "count",
                    "start": 6,
                    "end": 18,
                    "part": "seed",
                },
                {"part": "legume", "trait": "part", "start": 23, "end": 29},
            ],
        )

    def test_count_21(self):
        self.assertEqual(
            test("Racemes compact, 1- or 2- or 5-7-flowered"),
            [
                {"part": "inflorescence", "trait": "part", "start": 0, "end": 7},
                {
                    "min": 1,
                    "low": 2,
                    "high": 5,
                    "max": 7,
                    "trait": "count",
                    "start": 17,
                    "end": 32,
                    "part": "inflorescence",
                    "subpart": "flowered",
                },
                {
                    "subpart": "flowered",
                    "trait": "subpart",
                    "start": 32,
                    "end": 41,
                    "part": "inflorescence",
                },
            ],
        )

    def test_count_22(self):
        self.assertEqual(
            test("3(or 5-9)-foliolate;"),
            [
                {
                    "min": 3,
                    "low": 5,
                    "high": 9,
                    "trait": "count",
                    "start": 0,
                    "end": 9,
                    "subpart": "lobe",
                },
                {"subpart": "lobe", "trait": "subpart", "start": 9, "end": 19},
            ],
        )

    def test_count_23(self):
        self.assertEqual(
            test("leaflets (2or)3- or 4(or 5)-paired"),
            [
                {"part": "leaflet", "trait": "part", "start": 0, "end": 8},
                {
                    "min": 2,
                    "low": 3,
                    "high": 4,
                    "max": 5,
                    "count_group": "pair",
                    "trait": "count",
                    "start": 9,
                    "end": 34,
                    "part": "leaflet",
                },
            ],
        )

    def test_count_24(self):
        self.assertEqual(
            test("Leaves (19-)23- or 25-foliolate;"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 6},
                {
                    "min": 19,
                    "low": 23,
                    "high": 25,
                    "trait": "count",
                    "start": 7,
                    "end": 21,
                    "part": "leaf",
                    "subpart": "lobe",
                },
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 21,
                    "end": 31,
                    "part": "leaf",
                },
            ],
        )

    def test_count_25(self):
        self.assertEqual(
            test("Calyx (5-lobed)"),
            [
                {"part": "calyx", "trait": "part", "start": 0, "end": 5},
                {
                    "low": 5,
                    "trait": "count",
                    "part": "calyx",
                    "subpart": "lobe",
                    "start": 7,
                    "end": 8,
                },
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 8,
                    "end": 14,
                    "part": "calyx",
                },
            ],
        )

    def test_count_26(self):
        self.assertEqual(
            test("blade lobes 0 or 1–4(or 5) per side"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 5},
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 6,
                    "end": 11,
                    "part": "leaf",
                },
                {
                    "min": 0,
                    "low": 1,
                    "high": 4,
                    "max": 5,
                    "count_group": "per side",
                    "trait": "count",
                    "start": 12,
                    "end": 35,
                    "part": "leaf",
                    "subpart": "lobe",
                },
            ],
        )

    def test_count_27(self):
        self.assertEqual(
            test("stems (11–16) pairs"),
            [
                {"part": "stem", "trait": "part", "start": 0, "end": 5},
                {
                    "low": 11,
                    "high": 16,
                    "count_group": "pairs",
                    "trait": "count",
                    "start": 6,
                    "end": 19,
                    "part": "stem",
                },
            ],
        )

    def test_count_28(self):
        self.assertEqual(
            test("stamens 5–10 or 20."),
            [
                {"part": "stamen", "trait": "part", "start": 0, "end": 7},
                {
                    "low": 5,
                    "high": 10,
                    "max": 20,
                    "trait": "count",
                    "part": "stamen",
                    "start": 8,
                    "end": 18,
                },
            ],
        )

    def test_count_29(self):
        self.assertEqual(
            test("blade lobes 0 or 1–4(–9) per side"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 5},
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 6,
                    "end": 11,
                    "part": "leaf",
                },
                {
                    "min": 0,
                    "low": 1,
                    "high": 4,
                    "max": 9,
                    "count_group": "per side",
                    "trait": "count",
                    "start": 12,
                    "end": 33,
                    "part": "leaf",
                    "subpart": "lobe",
                },
            ],
        )

    def test_count_30(self):
        self.assertEqual(
            test("Inflorescences 1–64(–90)[–100]-flowered"),
            [
                {"part": "inflorescence", "trait": "part", "start": 0, "end": 14},
                {
                    "min": 1,
                    "low": 64,
                    "high": 90,
                    "max": 100,
                    "trait": "count",
                    "part": "inflorescence",
                    "subpart": "flowered",
                    "start": 15,
                    "end": 30,
                },
                {
                    "subpart": "flowered",
                    "trait": "subpart",
                    "start": 30,
                    "end": 39,
                    "part": "inflorescence",
                },
            ],
        )

    def test_count_31(self):
        self.assertEqual(
            test("sepals absent;"),
            [
                {"part": "sepal", "trait": "part", "start": 0, "end": 6},
                {"low": 0, "trait": "count", "part": "sepal", "start": 7, "end": 13},
            ],
        )

    def test_count_32(self):
        self.assertEqual(
            test(
                """
                staminate catkins in 1 or more clusters of 3--6;
                pistillate catkins in 1 or more clusters of 2--7
                """
            ),
            [
                {
                    "sex": "staminate",
                    "trait": "sex",
                    "start": 0,
                    "end": 9,
                    "part": "catkin",
                },
                {
                    "part": "catkin",
                    "trait": "part",
                    "start": 10,
                    "end": 17,
                    "sex": "staminate",
                },
                {
                    "low": 1,
                    "trait": "count",
                    "start": 21,
                    "end": 22,
                    "part": "catkin",
                    "sex": "staminate",
                },
                {
                    "low": 3,
                    "high": 6,
                    "trait": "count",
                    "start": 43,
                    "end": 47,
                    "part": "catkin",
                    "sex": "staminate",
                },
                {
                    "sex": "pistillate",
                    "trait": "sex",
                    "start": 49,
                    "end": 59,
                    "part": "catkin",
                },
                {
                    "part": "catkin",
                    "trait": "part",
                    "start": 60,
                    "end": 67,
                    "sex": "pistillate",
                },
                {
                    "low": 1,
                    "trait": "count",
                    "start": 71,
                    "end": 72,
                    "part": "catkin",
                    "sex": "pistillate",
                },
                {
                    "low": 2,
                    "high": 7,
                    "trait": "count",
                    "start": 93,
                    "end": 97,
                    "part": "catkin",
                    "sex": "staminate",
                },
            ],
        )

    def test_count_33(self):
        self.assertEqual(
            test("""Cymes [1–]few[–many]-flowered."""),
            [
                {"part": "cyme", "trait": "part", "start": 0, "end": 5},
                {
                    "low": 1,
                    "trait": "count",
                    "start": 6,
                    "end": 20,
                    "part": "cyme",
                    "subpart": "flowered",
                },
                {
                    "subpart": "flowered",
                    "trait": "subpart",
                    "start": 20,
                    "end": 29,
                    "part": "cyme",
                },
            ],
        )

    def test_count_34(self):
        self.assertEqual(
            test("""Capsules [2–]3[–5+]-locular."""),
            [
                {"part": "capsule", "trait": "part", "start": 0, "end": 8},
                {
                    "min": 2,
                    "low": 3,
                    "max": 5,
                    "trait": "count",
                    "start": 9,
                    "end": 19,
                    "part": "capsule",
                    "subpart": "locular",
                },
                {
                    "subpart": "locular",
                    "trait": "subpart",
                    "start": 19,
                    "end": 27,
                    "part": "capsule",
                },
            ],
        )

    def test_count_35(self):
        self.assertEqual(
            test("""Capsule 2-locular. x = 9."""),
            [
                {"part": "capsule", "trait": "part", "start": 0, "end": 7},
                {
                    "low": 2,
                    "trait": "count",
                    "start": 8,
                    "end": 9,
                    "part": "capsule",
                    "subpart": "locular",
                },
                {
                    "subpart": "locular",
                    "trait": "subpart",
                    "start": 9,
                    "end": 17,
                    "part": "capsule",
                },
                {"part": "x", "trait": "part", "start": 19, "end": 22},
                {"low": 9, "trait": "count", "start": 23, "end": 24, "part": "x"},
            ],
        )

    def test_count_36(self):
        self.assertEqual(
            test("Seeds 1000"),
            [{"end": 5, "part": "seed", "start": 0, "trait": "part"}],
        )
