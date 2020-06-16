"""Test attaching traits to plant parts."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.util import shorten

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestAttach(unittest.TestCase):
    """Test attaching traits to plant parts."""

    def test_attach_01(self):
        self.assertEqual(
            MATCHER.parse(
                'keel with blue tip; standard 8-9 × ca. 6 mm, '
                'widely elliptic, emarginate; wings'),
            {'subpart': [{'subpart': 'keel', 'start': 0, 'end': 4},
                         {'subpart': 'wing', 'start': 74, 'end': 79}],
             'plant_keel_color': [
                 {'color': 'blue-tip', 'start': 10, 'end': 18}],
             'plant_keel_size': [{'start': 39, 'end': 43,
                                  'length_low': 6, 'length_units': 'mm'}],
             'plant_keel_shape': [
                 {'shape': 'elliptic', 'start': 52, 'end': 60},
                 {'shape': 'emarginate', 'start': 62, 'end': 72}]}
        )

    def test_attach_02(self):
        self.assertEqual(
            MATCHER.parse(shorten("""
                Calyx ca. 5 mm, loosely to rather densely appressed hairy;
                teeth ca. 2.5 mm.
                """)),
            {'part': [{'start': 0, 'end': 5, 'part': 'calyx'}],
             'calyx_size': [{'start': 10, 'end': 14,
                             'length_low': 5, 'length_units': 'mm'}],
             'subpart': [{'subpart': 'tooth', 'start': 59, 'end': 64}],
             'calyx_tooth_size': [{'start': 69, 'end': 75,
                                   'length_low': 2.5, 'length_units': 'mm'}]}
        )

    def test_attach_03(self):
        self.assertEqual(
            MATCHER.parse(shorten("""
                Plants to 30 cm tall, strongly branched, with appressed to 
                spreading only white hairs 0.2-1.5 mm, at calyx up to 3 mm.
                Calyx 12-15 mm, hairy; teeth 2-5 mm.
                """)),
            {'part': [{'start': 0, 'end': 6, 'part': 'plant'},
                      {'start': 101, 'end': 106, 'part': 'calyx'},
                      {'start': 119, 'end': 124, 'part': 'calyx'}],
             'plant_size': [{'start': 7, 'end': 20,
                             'height_high': 30, 'height_units': 'cm'}],
             'plant_hair_color': [{'color': 'white', 'start': 74, 'end': 79}],
             'subpart': [{'subpart': 'hair', 'start': 80, 'end': 85},
                         {'subpart': 'tooth', 'start': 142, 'end': 147}],
             'plant_hair_size': [{'start': 86, 'end': 96, 'length_low': 0.2,
                                  'length_high': 1.5, 'length_units': 'mm'}],
             'calyx_hair_size': [{'start': 110, 'end': 117,
                                  'length_high': 3, 'length_units': 'mm'}],
             'calyx_size': [{'start': 125, 'end': 133, 'length_low': 12,
                             'length_high': 15, 'length_units': 'mm'}],
             'calyx_tooth_size': [{'start': 148, 'end': 154, 'length_low': 2,
                                   'length_high': 5, 'length_units': 'mm'}]}
        )

    def test_attach_04(self):
        self.assertEqual(
            MATCHER.parse(shorten("""
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

    def test_attach_05(self):
        self.assertEqual(
            MATCHER.parse(shorten("""
                Calyx 10-12 mm, densely covered with extremely asymmetrically
                bifurcate to basifixed, spreading hairs 1-2 mm; teeth ca.
                4 mm. Petals white; standard oblong-pandurate, ca. 25 × 8 mm,
                in lower 1/3 slightly constricted, base widened,
                hastate-auriculate, apex emarginate;""")),
            {'part': [{'start': 0, 'end': 5, 'part': 'calyx'},
                      {'start': 126, 'end': 132, 'part': 'petal'}],
             'calyx_size': [{'start': 6, 'end': 14, 'length_low': 10,
                             'length_high': 12, 'length_units': 'mm'}],
             'subpart': [{'subpart': 'hair', 'start': 96, 'end': 101},
                         {'subpart': 'tooth', 'start': 110, 'end': 115},
                         {'subpart': 'base', 'start': 217, 'end': 221},
                         {'subpart': 'apex', 'start': 251, 'end': 255}],
             'calyx_hair_size': [{'start': 102, 'end': 108,
                                  'length_low': 1, 'length_high': 2,
                                  'length_units': 'mm'}],
             'calyx_tooth_size': [{'start': 120, 'end': 124, 'length_low': 4,
                                   'length_units': 'mm'}],
             'petal_color': [{'color': 'white', 'start': 133, 'end': 138}],
             'petal_shape': [
                 {'shape': 'oblong-pandurate', 'start': 149, 'end': 165}],
             'petal_size': [{'start': 171, 'end': 180, 'length_low': 25,
                             'width_low': 8, 'width_units': 'mm'}],
             'petal_base_shape': [{'shape': 'hastate-auriculate',
                                   'start': 231, 'end': 249}],
             'petal_apex_shape': [
                 {'shape': 'emarginate', 'start': 256, 'end': 266}]}
        )

    def test_attach_06(self):
        self.assertEqual(
            MATCHER.parse(shorten("""
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
