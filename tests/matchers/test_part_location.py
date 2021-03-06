"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from tests.setup import test


class TestPartLocation(unittest.TestCase):
    """Test the plant part parser."""

    def test_part_location_01(self):
        self.assertEqual(
            test('stipules 3-8 mm, semiamplexicaul, adnate to petiole for 1-2 mm'),
            [{'part': 'stipule', 'trait': 'part', 'start': 0, 'end': 8},
             {'length_low': 3, 'length_high': 8, 'length_units': 'mm',
              'trait': 'size', 'part': 'stipule',
              'start': 9, 'end': 15}]
        )

    def test_part_location_02(self):
        self.assertEqual(
            test('completely embracing stem but not connate'),
            [{'shape': 'not connate',
              'trait': 'shape', 'part': 'plant', 'start': 30, 'end': 41}]
        )

    def test_part_location_03(self):
        self.assertEqual(
            test('stipules shortly ciliate at margin'),
            [{'part': 'stipule', 'trait': 'part', 'start': 0, 'end': 8},
             {'margin_shape': 'ciliate',
              'trait': 'margin_shape', 'part': 'stipule',
              'start': 17, 'end': 24},
             {'subpart': 'margin', 'trait': 'subpart', 'part': 'stipule',
              'start': 28, 'end': 34}]
        )
