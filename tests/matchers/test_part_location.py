"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from src.pylib.pipeline import PIPELINE

NLP = PIPELINE.trait_list


class TestPartLocation(unittest.TestCase):
    """Test the plant part parser."""

    def test_part_location_01(self):
        self.assertEqual(
            NLP('stipules 3-8 mm, semiamplexicaul, adnate to petiole for '
                '1-2 mm'),
            [{'part': 'stipule', 'trait': 'part', 'start': 0, 'end': 8},
             {'length_low': 3,
              'length_high': 8,
              'length_units': 'mm',
              'trait': 'stipule_size',
              'start': 9,
              'end': 15}]
        )

    def test_part_location_02(self):
        self.assertEqual(
            NLP('completely embracing stem but not connate'),
            [{'shape': 'not connate',
              'trait': 'plant_shape', 'start': 30, 'end': 41}]
        )
