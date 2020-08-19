"""Test attaching traits to plant parts."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten

from efloras.pylib.pipeline import parse


class TestAttachFSM(unittest.TestCase):
    """Test attaching traits to plant parts."""

    def test_attach_fsm_01(self):
        self.assertEqual(
            parse(
                'Petals purple, keel with blue tip; standard 8-9 × ca. 6 mm, '
                'widely elliptic, emarginate;'),
            [{'part': 'petal', 'trait': 'part', 'start': 0, 'end': 6},
             {'color': 'purple', 'trait': 'petal_color', 'start': 7,
              'end': 13},
             {'subpart': 'keel', 'trait': 'subpart', 'start': 15, 'end': 19},
             {'color': 'blue-tip', 'trait': 'petal_keel_color', 'start': 25,
              'end': 33},
             {'length_low': 8,
              'length_high': 9,
              'width_low': 6,
              'width_units': 'mm',
              'trait': 'petal_size',
              'start': 44,
              'end': 58},
             {'shape': 'elliptic', 'trait': 'petal_shape', 'start': 67,
              'end': 75},
             {'shape': 'emarginate', 'trait': 'petal_shape', 'start': 77,
              'end': 87}]
        )

    def test_attach_fsm_02(self):
        self.assertEqual(
            parse(shorten("""
                Calyx ca. 5 mm, loosely to rather densely appressed hairy;
                teeth ca. 2.5 mm.
                """)),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 5,
              'length_units': 'mm',
              'trait': 'calyx_size',
              'start': 6,
              'end': 14},
             {'subpart': 'tooth', 'trait': 'subpart', 'start': 59, 'end': 64},
             {'length_low': 2.5,
              'length_units': 'mm',
              'trait': 'calyx_tooth_size',
              'start': 65,
              'end': 75}]
        )

    def test_attach_fsm_03(self):
        self.assertEqual(
            parse(shorten("""
                Plants to 30 cm tall, strongly branched, with appressed to 
                spreading only white hairs 0.2-1.5 mm, at calyx up to 3 mm.
                """)),
            [{'part': 'plant', 'trait': 'part', 'start': 0, 'end': 6},
             {'height_high': 30,
              'height_units': 'cm',
              'trait': 'plant_size',
              'start': 7,
              'end': 20},
             {'color': 'white', 'trait': 'plant_hair_color', 'start': 74,
              'end': 79},
             {'subpart': 'hair', 'trait': 'subpart', 'start': 80, 'end': 85},
             {'length_low': 0.2,
              'length_high': 1.5,
              'length_units': 'mm',
              'trait': 'plant_hair_size',
              'start': 86,
              'end': 96},
             {'length_high': 3,
              'length_units': 'mm',
              'trait': 'plant_hair_size',
              'start': 110,
              'end': 117}]
        )

    def test_attach_fsm_04(self):
        self.assertEqual(
            parse(shorten("""
                Calyx shortly tubular, 8-9 mm, subglabrous or in upper part
                with short spreading black hairs; teeth nearly equal, narrowly
                triangular, 0.8-1 mm.""")),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'shape': 'tubular', 'trait': 'calyx_shape', 'start': 14,
              'end': 21},
             {'length_low': 8,
              'length_high': 9,
              'length_units': 'mm',
              'trait': 'calyx_size',
              'start': 23,
              'end': 29},
             {'color': 'black', 'trait': 'calyx_hair_color', 'start': 81,
              'end': 86},
             {'subpart': 'hair', 'trait': 'subpart', 'start': 87, 'end': 92},
             {'subpart': 'tooth', 'trait': 'subpart', 'start': 94, 'end': 99},
             {'shape': 'triangular',
              'trait': 'calyx_tooth_shape',
              'start': 114,
              'end': 133},
             {'length_low': 0.8,
              'length_high': 1.0,
              'length_units': 'mm',
              'trait': 'calyx_tooth_size',
              'start': 135,
              'end': 143}]
        )

    def test_attach_fsm_05(self):
        self.assertEqual(
            parse(shorten("""
                Calyx 10-12 mm, densely covered with extremely asymmetrically
                bifurcate to basifixed, spreading hairs 1-2 mm; teeth ca.
                4 mm. Petals white; standard oblong-pandurate, ca. 25 × 8 mm,
                in lower 1/3 slightly constricted, base widened,
                hastate-auriculate, apex emarginate;""")),
            [{'part': 'calyx', 'trait': 'part', 'start': 0, 'end': 5},
             {'length_low': 10,
              'length_high': 12,
              'length_units': 'mm',
              'trait': 'calyx_size',
              'start': 6,
              'end': 14},
             {'subpart': 'hair', 'trait': 'subpart', 'start': 96, 'end': 101},
             {'length_low': 1,
              'length_high': 2,
              'length_units': 'mm',
              'trait': 'calyx_hair_size',
              'start': 102,
              'end': 108},
             {'subpart': 'tooth', 'trait': 'subpart', 'start': 110,
              'end': 115},
             {'length_low': 4,
              'length_units': 'mm',
              'trait': 'calyx_tooth_size',
              'start': 116,
              'end': 124},
             {'part': 'petal', 'trait': 'part', 'start': 126, 'end': 132},
             {'color': 'white', 'trait': 'petal_color', 'start': 133,
              'end': 138},
             {'shape': 'oblong-pandurate',
              'trait': 'petal_shape',
              'start': 149,
              'end': 165},
             {'length_low': 25,
              'width_low': 8,
              'width_units': 'mm',
              'trait': 'petal_size',
              'start': 167,
              'end': 180},
             {'subpart': 'base', 'trait': 'subpart', 'start': 217, 'end': 221},
             {'shape': 'hastate-auriculate',
              'trait': 'petal_base_shape',
              'start': 231,
              'end': 249},
             {'subpart': 'apex', 'trait': 'subpart', 'start': 251, 'end': 255},
             {'shape': 'emarginate', 'trait': 'petal_apex_shape', 'start': 256,
              'end': 266}]
        )

    def test_attach_fsm_06(self):
        self.assertEqual(
            parse(shorten("""
                Racemes short, 3-9-flowered; peduncle 0.5-2 cm, loosely to
                rather densely hairy; bracts 0.5-1 mm, white hairy.""")),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 7},
             {'low': 3,
              'high': 9,
              'trait': 'inflorescence_flower_count',
              'start': 15,
              'end': 27},
             {'part': 'peduncle', 'trait': 'part', 'start': 29, 'end': 37},
             {'length_low': 0.5,
              'length_high': 2.0,
              'length_units': 'cm',
              'trait': 'peduncle_size',
              'start': 38,
              'end': 46},
             {'part': 'bract', 'trait': 'part', 'start': 81, 'end': 87},
             {'length_low': 0.5,
              'length_high': 1.0,
              'length_units': 'mm',
              'trait': 'bract_size',
              'start': 88,
              'end': 96},
             {'color': 'white', 'trait': 'bract_color', 'start': 98,
              'end': 103}]
        )

    def test_attach_fsm_07(self):
        self.assertEqual(
            parse(shorten("""
                hypanthium  pistillodes with 3-lobed ovary.""")),
            [{'part': 'hypanthium', 'trait': 'part', 'start': 0, 'end': 10},
             {'part': 'pistol', 'trait': 'part', 'start': 11, 'end': 22},
             {'low': 3, 'trait': 'ovary_lobe_count', 'start': 28, 'end': 35},
             {'part': 'ovary', 'trait': 'part', 'start': 36, 'end': 41}]
        )

    def test_attach_fsm_08(self):
        self.assertEqual(
            parse(shorten('roots thin, without thick, woody rootstock')),
            [{'part': 'root', 'trait': 'part', 'start': 0, 'end': 5},
             {'woodiness': 'not woody',
              'trait': 'rootstock_woodiness',
              'start': 27,
              'end': 32},
             {'part': 'rootstock', 'trait': 'part', 'start': 33, 'end': 42}]
        )

    def test_attach_fsm_09(self):
        self.assertEqual(
            parse(shorten("""
                Legumes with a stipe 6-7 mm, pen­dulous, narrowly ellipsoid,
                1.5-2.4 cm, 6-7 mm wide and 4-5 mm high,""")),
            [{'part': 'legume', 'trait': 'part', 'start': 0, 'end': 7},
             {'length_low': 6,
              'length_high': 7,
              'length_units': 'mm',
              'trait': 'legume_stipe_size',
              'start': 8,
              'end': 27},
             {'shape': 'ellipsoid', 'trait': 'legume_shape', 'start': 41,
              'end': 59},
             {'length_low': 1.5,
              'length_high': 2.4,
              'length_units': 'cm',
              'trait': 'legume_size',
              'start': 61,
              'end': 71},
             {'width_low': 6,
              'width_high': 7,
              'width_units': 'mm',
              'trait': 'legume_size',
              'start': 73,
              'end': 84},
             {'height_low': 4,
              'height_high': 5,
              'height_units': 'mm',
              'trait': 'legume_size',
              'start': 89,
              'end': 100}]
        )
