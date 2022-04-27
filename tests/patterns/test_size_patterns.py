"""Test plant size trait matcher."""
# pylint: disable=missing-function-docstring, too-many-public-methods
import unittest

from tests.setup import test


class TestSize(unittest.TestCase):
    """Test plant size trait parsers."""

    # def test_size_00(self):
    #     test('Leaf (12-)23-34 × 45-56 cm wide')

    def test_size_01(self):
        self.assertEqual(
            test("Leaf (12-)23-34 × 45-56 cm"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 4},
                {
                    "length_min": 12.0,
                    "length_low": 23.0,
                    "length_high": 34.0,
                    "length_units": "cm",
                    "width_low": 45.0,
                    "width_high": 56.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 5,
                    "end": 26,
                    "part": "leaf",
                },
            ],
        )

    def test_size_02(self):
        self.assertEqual(
            test("leaf (12-)23-34 × 45-56"),
            [{"part": "leaf", "trait": "part", "start": 0, "end": 4}],
        )

    def test_size_03(self):
        self.assertEqual(
            test("blade 1.5–5(–7) cm"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 5},
                {
                    "length_low": 1.5,
                    "length_high": 5.0,
                    "length_max": 7.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 6,
                    "end": 18,
                    "part": "leaf",
                },
            ],
        )

    def test_size_04(self):
        self.assertEqual(
            test("leaf shallowly to deeply 5–7-lobed"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 4},
                {
                    "low": 5,
                    "high": 7,
                    "trait": "count",
                    "start": 25,
                    "end": 28,
                    "part": "leaf",
                    "subpart": "lobe",
                },
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 28,
                    "end": 34,
                    "part": "leaf",
                },
            ],
        )

    def test_size_05(self):
        self.assertEqual(
            test("leaf 4–10 cm wide"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 4},
                {
                    "width_low": 4.0,
                    "width_high": 10.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 5,
                    "end": 17,
                    "part": "leaf",
                },
            ],
        )

    def test_size_06(self):
        self.assertEqual(
            test("leaf sinuses 1/5–1/4 to base"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 4},
                {
                    "subpart": "sinus",
                    "trait": "subpart",
                    "start": 5,
                    "end": 12,
                    "part": "leaf",
                },
                {
                    "subpart_location": "to base",
                    "trait": "part_as_loc",
                    "start": 21,
                    "end": 28,
                    "part": "leaf",
                    "subpart": "sinus",
                },
            ],
        )

    def test_size_07(self):
        self.assertEqual(
            test("petiolules 2–5 mm"),
            [
                {"part": "petiolule", "trait": "part", "start": 0, "end": 10},
                {
                    "length_low": 2.0,
                    "length_high": 5.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 11,
                    "end": 17,
                    "part": "petiolule",
                },
            ],
        )

    def test_size_08(self):
        self.assertEqual(
            test("petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm."),
            [
                {"part": "petiolule", "trait": "part", "start": 0, "end": 10},
                {
                    "length_low": 2.0,
                    "length_high": 5.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 11,
                    "end": 17,
                    "part": "petiolule",
                },
                {
                    "margin_shape": "serrate",
                    "trait": "margin_shape",
                    "start": 19,
                    "end": 35,
                    "part": "petiole",
                },
                {"part": "petiole", "trait": "part", "start": 37, "end": 45},
                {
                    "length_low": 16.0,
                    "length_high": 28.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 46,
                    "end": 55,
                    "part": "petiole",
                },
            ],
        )

    def test_size_09(self):
        self.assertEqual(
            test("Leaves: petiole 2–15 cm;"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 6},
                {"part": "petiole", "trait": "part", "start": 8, "end": 15},
                {
                    "length_low": 2.0,
                    "length_high": 15.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 16,
                    "end": 23,
                    "part": "petiole",
                },
            ],
        )

    def test_size_10(self):
        self.assertEqual(
            test("petiole [5–]7–25[–32] mm, glabrous,"),
            [
                {"part": "petiole", "trait": "part", "start": 0, "end": 7},
                {
                    "length_min": 5.0,
                    "length_low": 7.0,
                    "length_high": 25.0,
                    "length_max": 32.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 8,
                    "end": 24,
                    "part": "petiole",
                },
            ],
        )

    def test_size_11(self):
        self.assertEqual(
            test("leaf 2–4 cm × 2–10 mm"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 4},
                {
                    "length_low": 2.0,
                    "length_high": 4.0,
                    "length_units": "cm",
                    "width_low": 2.0,
                    "width_high": 10.0,
                    "width_units": "mm",
                    "trait": "size",
                    "start": 5,
                    "end": 21,
                    "part": "leaf",
                },
            ],
        )

    def test_size_12(self):
        self.assertEqual(
            test("leaf deeply to shallowly lobed, 4–5(–7) cm wide,"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 4},
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 25,
                    "end": 30,
                    "part": "leaf",
                },
                {
                    "width_low": 4.0,
                    "width_high": 5.0,
                    "width_max": 7.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 32,
                    "end": 47,
                    "part": "leaf",
                    "subpart": "lobe",
                },
            ],
        )

    def test_size_13(self):
        self.assertEqual(
            test(
                """
                Leaves 3-foliolate, lateral pair of leaflets
                deeply lobed, petiolules 2–5 mm,"""
            ),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 6},
                {
                    "low": 3,
                    "trait": "count",
                    "start": 7,
                    "end": 8,
                    "part": "leaf",
                    "subpart": "lobe",
                },
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 8,
                    "end": 18,
                    "part": "leaf",
                },
                {
                    "location": "lateral",
                    "trait": "location",
                    "start": 20,
                    "end": 27,
                    "part": "leaf",
                    "subpart": "lobe",
                },
                {"part": "leaflet", "trait": "part", "start": 36, "end": 44},
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 52,
                    "end": 57,
                    "part": "leaflet",
                },
                {"part": "petiolule", "trait": "part", "start": 59, "end": 69},
                {
                    "length_low": 2.0,
                    "length_high": 5.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 70,
                    "end": 76,
                    "part": "petiolule",
                    "subpart": "lobe",
                },
            ],
        )

    def test_size_14(self):
        self.assertEqual(
            test("terminal leaflet 3–5 cm, blade petiolule 3–12 mm,"),
            [
                {
                    "location": "terminal",
                    "trait": "location",
                    "start": 0,
                    "end": 8,
                    "part": "leaflet",
                },
                {
                    "part": "leaflet",
                    "trait": "part",
                    "start": 9,
                    "end": 16,
                    "location": "terminal",
                },
                {
                    "length_low": 3.0,
                    "length_high": 5.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 17,
                    "end": 23,
                    "location": "terminal",
                    "part": "leaflet",
                },
                {
                    "part": "leaf",
                    "trait": "part",
                    "start": 25,
                    "end": 30,
                    "location": "terminal",
                },
                {
                    "part": "petiolule",
                    "trait": "part",
                    "start": 31,
                    "end": 40,
                    "location": "terminal",
                },
                {
                    "length_low": 3.0,
                    "length_high": 12.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 41,
                    "end": 48,
                    "location": "terminal",
                    "part": "petiolule",
                },
            ],
        )

    def test_size_15(self):
        self.assertEqual(
            test("leaf shallowly 3–5(–7)-lobed, 5–25 × (8–)10–25(–30) cm,"),
            [
                {"part": "leaf", "trait": "part", "start": 0, "end": 4},
                {
                    "low": 3,
                    "high": 5,
                    "max": 7,
                    "trait": "count",
                    "start": 15,
                    "end": 22,
                    "part": "leaf",
                },
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 22,
                    "end": 28,
                    "part": "leaf",
                },
                {
                    "length_low": 5.0,
                    "length_high": 25.0,
                    "length_units": "cm",
                    "width_min": 8.0,
                    "width_low": 10.0,
                    "width_high": 25.0,
                    "width_max": 30.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 30,
                    "end": 54,
                    "part": "leaf",
                    "subpart": "lobe",
                },
            ],
        )

    def test_size_16(self):
        self.assertEqual(
            test("(3–)5-lobed, 6–20(–30) × 6–25 cm,"),
            [
                {
                    "min": 3,
                    "low": 5,
                    "trait": "count",
                    "start": 0,
                    "end": 5,
                    "subpart": "lobe",
                },
                {"subpart": "lobe", "trait": "subpart", "start": 5, "end": 11},
                {
                    "length_low": 6.0,
                    "length_high": 20.0,
                    "length_max": 30.0,
                    "length_units": "cm",
                    "width_low": 6.0,
                    "width_high": 25.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 13,
                    "end": 32,
                    "subpart": "lobe",
                },
            ],
        )

    def test_size_17(self):
        self.assertEqual(
            test("petiole to 11 cm;"),
            [
                {"part": "petiole", "trait": "part", "start": 0, "end": 7},
                {
                    "length_high": 11.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 8,
                    "end": 16,
                    "part": "petiole",
                },
            ],
        )

    def test_size_18(self):
        self.assertEqual(
            test("petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate)"),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {
                    "length_min": 1.0,
                    "length_low": 3.0,
                    "length_high": 10.0,
                    "length_max": 12.0,
                    "length_units": "mm",
                    "sex": "pistillate",
                    "trait": "size",
                    "start": 7,
                    "end": 36,
                    "part": "petal",
                },
                {
                    "length_low": 5.0,
                    "length_high": 8.0,
                    "length_max": 10.0,
                    "length_units": "mm",
                    "sex": "staminate",
                    "trait": "size",
                    "start": 40,
                    "end": 63,
                    "part": "petal",
                },
            ],
        )

    def test_size_19(self):
        self.assertEqual(
            test("Flowers 5–10 cm diam.; hypanthium 4–8 mm,"),
            [
                {"part": "flower", "trait": "part", "start": 0, "end": 7},
                {
                    "diameter_low": 5.0,
                    "diameter_high": 10.0,
                    "diameter_units": "cm",
                    "trait": "size",
                    "start": 8,
                    "end": 21,
                    "part": "flower",
                },
                {"part": "hypanthium", "trait": "part", "start": 23, "end": 33},
                {
                    "length_low": 4.0,
                    "length_high": 8.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 34,
                    "end": 40,
                    "part": "hypanthium",
                },
            ],
        )

    def test_size_20(self):
        self.assertEqual(
            test("Flowers 5--16 × 4--12 cm"),
            [
                {"part": "flower", "trait": "part", "start": 0, "end": 7},
                {
                    "length_low": 5.0,
                    "length_high": 16.0,
                    "length_units": "cm",
                    "width_low": 4.0,
                    "width_high": 12.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 8,
                    "end": 24,
                    "part": "flower",
                },
            ],
        )

    def test_size_21(self):
        self.assertEqual(
            test(
                """
                Inflorescences formed season before flowering and exposed
                during winter; staminate catkins 3--8.5 cm,"""
            ),
            [
                {"part": "inflorescence", "trait": "part", "start": 0, "end": 14},
                {
                    "sex": "staminate",
                    "trait": "sex",
                    "start": 73,
                    "end": 82,
                    "part": "catkin",
                },
                {
                    "part": "catkin",
                    "trait": "part",
                    "start": 83,
                    "end": 90,
                    "sex": "staminate",
                },
                {
                    "length_low": 3.0,
                    "length_high": 8.5,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 91,
                    "end": 100,
                    "part": "catkin",
                    "sex": "staminate",
                },
            ],
        )

    def test_size_22(self):
        self.assertEqual(
            test("Leaflets petiolulate; blade ovate, 8-15 × 4-15 cm,"),
            [
                {"part": "leaflet", "trait": "part", "start": 0, "end": 8},
                {"part": "leaf", "trait": "part", "start": 22, "end": 27},
                {
                    "shape": "ovate",
                    "trait": "shape",
                    "start": 28,
                    "end": 33,
                    "part": "leaf",
                },
                {
                    "length_low": 8.0,
                    "length_high": 15.0,
                    "length_units": "cm",
                    "width_low": 4.0,
                    "width_high": 15.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 35,
                    "end": 49,
                    "part": "leaf",
                },
            ],
        )

    def test_size_23(self):
        self.assertEqual(
            test("calyx, 8-10 mm, 3-4 mm high,"),
            [
                {"part": "calyx", "trait": "part", "start": 0, "end": 5},
                {
                    "length_low": 8.0,
                    "length_high": 10.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 7,
                    "end": 14,
                    "part": "calyx",
                },
                {
                    "height_low": 3.0,
                    "height_high": 4.0,
                    "height_units": "mm",
                    "trait": "size",
                    "start": 16,
                    "end": 27,
                    "part": "calyx",
                },
            ],
        )

    def test_size_24(self):
        self.assertEqual(
            test("Petals 15-21 × ca. 8 mm,"),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {
                    "length_low": 15.0,
                    "length_high": 21.0,
                    "length_units": "mm",
                    "width_low": 8.0,
                    "width_units": "mm",
                    "trait": "size",
                    "start": 7,
                    "end": 23,
                    "part": "petal",
                },
            ],
        )

    def test_size_25(self):
        self.assertEqual(
            test("Petals ca 8 mm."),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {
                    "length_low": 8.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 7,
                    "end": 15,
                    "part": "petal",
                },
            ],
        )

    def test_size_26(self):
        self.assertEqual(
            test("Legumes 7-10 mm, 2.8-4.5 mm high and wide"),
            [
                {"part": "legume", "trait": "part", "start": 0, "end": 7},
                {
                    "height_low": 7.0,
                    "height_high": 10.0,
                    "trait": "size",
                    "start": 8,
                    "end": 41,
                    "width_low": 2.8,
                    "width_high": 4.5,
                    "part": "legume",
                },
            ],
        )

    def test_size_27(self):
        self.assertEqual(
            test("Racemes 3-4 cm,"),
            [
                {"part": "inflorescence", "trait": "part", "start": 0, "end": 7},
                {
                    "length_low": 3.0,
                    "length_high": 4.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 8,
                    "end": 14,
                    "part": "inflorescence",
                },
            ],
        )

    def test_size_28(self):
        self.assertEqual(
            test("Petals pale violet, with darker keel; standard elliptic, 6-7 × 3-4;"),
            [
                {"part": "petal", "trait": "part", "start": 0, "end": 6},
                {
                    "color": "purple",
                    "trait": "color",
                    "start": 7,
                    "end": 18,
                    "part": "petal",
                },
                {
                    "subpart": "keel",
                    "trait": "subpart",
                    "start": 32,
                    "end": 36,
                    "part": "petal",
                },
                {
                    "shape": "elliptic",
                    "trait": "shape",
                    "start": 47,
                    "end": 55,
                    "part": "petal",
                },
            ],
        )

    def test_size_29(self):
        self.assertEqual(
            test("Seeds ca. 1.6 × 1-1.3 × 0.7-0.8 cm; hilum 8-10 mm."),
            [
                {"part": "seed", "trait": "part", "start": 0, "end": 5},
                {
                    "length_low": 1.6,
                    "length_units": "cm",
                    "width_low": 1.0,
                    "width_high": 1.3,
                    "width_units": "cm",
                    "thickness_low": 0.7,
                    "thickness_high": 0.8,
                    "thickness_units": "cm",
                    "trait": "size",
                    "start": 6,
                    "end": 34,
                    "part": "seed",
                    "subpart": "hilum",
                },
                {
                    "subpart": "hilum",
                    "trait": "subpart",
                    "start": 36,
                    "end": 41,
                    "part": "seed",
                },
                {
                    "length_low": 8.0,
                    "length_high": 10.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 42,
                    "end": 50,
                    "part": "seed",
                    "subpart": "hilum",
                },
            ],
        )

    def test_size_30(self):
        self.assertEqual(
            test("leaflets obovate, 1-2.5 × to 1.6 cm,"),
            [
                {"part": "leaflet", "trait": "part", "start": 0, "end": 8},
                {
                    "shape": "obovate",
                    "trait": "shape",
                    "start": 9,
                    "end": 16,
                    "part": "leaflet",
                },
                {
                    "length_low": 1.0,
                    "length_high": 2.5,
                    "length_units": "cm",
                    "width_low": 1.6,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 18,
                    "end": 35,
                    "part": "leaflet",
                },
            ],
        )

    def test_size_31(self):
        self.assertEqual(
            test("Shrubs, 0.5–1[–2.5] m."),
            [
                {"part": "shrub", "trait": "part", "start": 0, "end": 6},
                {
                    "length_low": 0.5,
                    "length_high": 1.0,
                    "length_max": 2.5,
                    "length_units": "m",
                    "trait": "size",
                    "part": "shrub",
                    "start": 8,
                    "end": 22,
                },
            ],
        )

    def test_size_32(self):
        self.assertEqual(
            test("trunk to 3(?) cm d.b.h.;"),
            [
                {"part": "trunk", "trait": "part", "start": 0, "end": 5},
                {
                    "dbh_high": 3.0,
                    "dbh_units": "cm",
                    "uncertain": "true",
                    "trait": "size",
                    "start": 6,
                    "end": 23,
                    "part": "trunk",
                },
            ],
        )

    def test_size_33(self):
        self.assertEqual(
            test("Trees to 25 m tall; bark yellow-brown, fissured."),
            [
                {"part": "tree", "trait": "part", "start": 0, "end": 5},
                {
                    "height_high": 25.0,
                    "height_units": "m",
                    "trait": "size",
                    "start": 6,
                    "end": 18,
                    "part": "tree",
                },
                {"part": "bark", "trait": "part", "start": 20, "end": 24},
                {
                    "color": "yellow-brown",
                    "trait": "color",
                    "start": 25,
                    "end": 37,
                    "part": "bark",
                },
            ],
        )

    def test_size_34(self):
        self.assertEqual(
            test("Shrubs or trees , 3-50 m. Bark light to dark gray"),
            [
                {"part": "shrub", "trait": "part", "start": 0, "end": 6},
                {"part": "tree", "trait": "part", "start": 10, "end": 15},
                {
                    "length_low": 3.0,
                    "length_high": 50.0,
                    "length_units": "m",
                    "trait": "size",
                    "start": 18,
                    "end": 25,
                    "part": "shrub",
                },
                {"part": "bark", "trait": "part", "start": 26, "end": 30},
                {
                    "color": "gray",
                    "trait": "color",
                    "start": 31,
                    "end": 49,
                    "part": "bark",
                },
            ],
        )
