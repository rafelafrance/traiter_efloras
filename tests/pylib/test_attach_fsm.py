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
            {'part': [{'part': 'petal', 'start': 0, 'end': 6}],
             'petal_color': [{'color': 'purple', 'start': 7, 'end': 13}],
             'subpart': [{'subpart': 'keel', 'start': 15, 'end': 19}],
             'petal_keel_color': [
                 {'color': 'blue-tip', 'start': 25, 'end': 33}],
             'petal_size': [{'length_low': 8, 'length_high': 9,
                             'width_low': 6, 'width_units': 'mm',
                             'start': 44, 'end': 58}],
             'petal_shape': [{'shape': 'elliptic', 'start': 67, 'end': 75},
                             {'shape': 'emarginate', 'start': 77, 'end': 87}]}
        )

    def test_attach_fsm_02(self):
        self.assertEqual(
            parse(shorten("""
                Calyx ca. 5 mm, loosely to rather densely appressed hairy;
                teeth ca. 2.5 mm.
                """)),
            {'part': [{'start': 0, 'end': 5, 'part': 'calyx'}],
             'calyx_size': [{'start': 6, 'end': 14, 'length_low': 5,
                             'length_units': 'mm'}],
             'subpart': [{'subpart': 'tooth', 'start': 59, 'end': 64}],
             'calyx_tooth_size': [{'start': 65, 'end': 75,
                                   'length_low': 2.5, 'length_units': 'mm'}]}
        )

    def test_attach_fsm_03(self):
        self.assertEqual(
            parse(shorten("""
                Plants to 30 cm tall, strongly branched, with appressed to 
                spreading only white hairs 0.2-1.5 mm, at calyx up to 3 mm.
                """)),
            {'part': [{'start': 0, 'end': 6, 'part': 'plant'}],
             'plant_size': [{'start': 7, 'end': 20,
                             'height_high': 30, 'height_units': 'cm'}],
             'plant_hair_color': [{'color': 'white', 'start': 74, 'end': 79}],
             'subpart': [{'subpart': 'hair', 'start': 80, 'end': 85}],
             'plant_hair_size': [
                 {'start': 86, 'end': 96, 'length_low': 0.2,
                  'length_high': 1.5, 'length_units': 'mm'},
                 {'start': 110, 'end': 117, 'length_high': 3.0,
                  'length_units': 'mm'}]}
        )

    def test_attach_fsm_04(self):
        self.assertEqual(
            parse(shorten("""
                Calyx shortly tubular, 8-9 mm, subglabrous or in upper part
                with short spreading black hairs; teeth nearly equal, narrowly
                triangular, 0.8-1 mm.""")),
            {'part': [{'start': 0, 'end': 5, 'part': 'calyx'}],
             'calyx_shape': [{'shape': 'tubular', 'start': 14, 'end': 21}],
             'calyx_size': [{'start': 23, 'end': 29, 'length_low': 8,
                             'length_high': 9, 'length_units': 'mm'}],
             'calyx_hair_color': [{'color': 'black', 'start': 81, 'end': 86}],
             'subpart': [{'subpart': 'hair', 'start': 87, 'end': 92},
                         {'subpart': 'tooth', 'start': 94, 'end': 99}],
             'calyx_tooth_shape': [
                 {'shape': 'triangular', 'start': 114, 'end': 133}],
             'calyx_tooth_size': [{'start': 135, 'end': 143, 'length_low': 0.8,
                                   'length_high': 1.0, 'length_units': 'mm'}]}
        )

    def test_attach_fsm_05(self):
        self.assertEqual(
            parse(shorten("""
                Calyx 10-12 mm, densely covered with extremely asymmetrically
                bifurcate to basifixed, spreading hairs 1-2 mm; teeth ca.
                4 mm. Petals white; standard oblong-pandurate, ca. 25 × 8 mm,
                in lower 1/3 slightly constricted, base widened,
                hastate-auriculate, apex emarginate;""")),
            {'part': [{'start': 0, 'end': 5, 'part': 'calyx'},
                      {'start': 126, 'end': 132, 'part': 'petal'}],
             'calyx_size': [{'start': 6, 'end': 14,
                             'length_low': 10, 'length_high': 12,
                             'length_units': 'mm'}],
             'subpart': [{'subpart': 'hair', 'start': 96, 'end': 101},
                         {'subpart': 'tooth', 'start': 110, 'end': 115},
                         {'subpart': 'base', 'start': 217, 'end': 221},
                         {'subpart': 'apex', 'start': 251, 'end': 255}],
             'calyx_hair_size': [{'start': 102, 'end': 108,
                                  'length_low': 1, 'length_high': 2,
                                  'length_units': 'mm'}],
             'calyx_tooth_size': [{'start': 116, 'end': 124,
                                   'length_low': 4, 'length_units': 'mm'}],
             'petal_color': [{'color': 'white', 'start': 133, 'end': 138}],
             'petal_shape': [
                 {'shape': 'oblong-pandurate', 'start': 149, 'end': 165}],
             'petal_size': [{'start': 167, 'end': 180,
                             'length_low': 25,
                             'width_low': 8, 'width_units': 'mm'}],
             'petal_base_shape': [{'shape': 'hastate-auriculate',
                                   'start': 231, 'end': 249}],
             'petal_apex_shape': [
                 {'shape': 'emarginate', 'start': 256, 'end': 266}]}
        )

    def test_attach_fsm_06(self):
        self.assertEqual(
            parse(shorten("""
                Racemes short, 3-9-flowered; peduncle 0.5-2 cm, loosely to
                rather densely hairy; bracts 0.5-1 mm, white hairy.""")),
            {'part': [{'start': 0, 'end': 7, 'part': 'inflorescence'},
                      {'start': 29, 'end': 37, 'part': 'peduncle'},
                      {'start': 81, 'end': 87, 'part': 'bract'}],
             'inflorescence_flower_count': [
                 {'start': 15, 'end': 27, 'low': 3, 'high': 9}],
             'peduncle_size': [{'start': 38, 'end': 46, 'length_low': 0.5,
                                'length_high': 2.0, 'length_units': 'cm'}],
             'bract_size': [{'start': 88, 'end': 96, 'length_low': 0.5,
                             'length_high': 1.0, 'length_units': 'mm'}],
             'bract_color': [{'color': 'white', 'start': 98, 'end': 103}]}
        )

    def test_attach_fsm_07(self):
        self.assertEqual(
            parse(shorten("""
                hypanthium  pistillodes with 3-lobed ovary.""")),
            {'part': [{'start': 0, 'end': 10, 'part': 'hypanthium'},
                      {'start': 11, 'end': 22, 'part': 'pistol'},
                      {'start': 36, 'end': 41, 'part': 'ovary'}],
             'ovary_lobe_count': [{'start': 28, 'end': 35, 'low': 3}]}
        )

    def test_attach_fsm_08(self):
        self.assertEqual(
            parse(shorten('roots thin, without thick, woody rootstock')),
            {'part': [{'start': 0, 'end': 5, 'part': 'root'},
                      {'start': 33, 'end': 42, 'part': 'rootstock'}],
             'rootstock_woodiness': [
                 {'start': 27, 'end': 32, 'woodiness': 'not woody'}]}
        )

    def test_attach_fsm_09(self):
        self.assertEqual(
            parse(shorten("""
                Legumes with a stipe 6-7 mm, pen­dulous, narrowly ellipsoid,
                1.5-2.4 cm, 6-7 mm wide and 4-5 mm high,""")),
            {'part': [{'part': 'legume', 'start': 0, 'end': 7}],
             'legume_stipe_size': [{'length_low': 6, 'length_high': 7,
                                    'length_units': 'mm',
                                    'start': 8, 'end': 27}],
             'legume_shape': [{'shape': 'ellipsoid', 'start': 41, 'end': 59}],
             'legume_size': [{'length_low': 1.5, 'length_high': 2.4,
                              'length_units': 'cm', 'start': 61, 'end': 71},
                             {'width_low': 6, 'width_high': 7,
                              'width_units': 'mm', 'start': 73, 'end': 84},
                             {'height_low': 4, 'height_high': 5,
                              'height_units': 'mm', 'start': 89, 'end': 100}]}
        )
