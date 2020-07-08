"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.pylib.pipeline import parse


class TestPartLocation(unittest.TestCase):
    """Test the plant part parser."""

    def test_part_location_01(self):
        self.assertEqual(
            parse(
                'stipules 3-8 mm, semiamplexicaul, adnate to petiole for '
                '1-2 mm'),
            {'part': [{'part': 'stipule', 'start': 0, 'end': 8}],
             'stipule_size': [{'length_low': 3, 'length_high': 8,
                               'length_units': 'mm', 'start': 9, 'end': 15}]}
        )
