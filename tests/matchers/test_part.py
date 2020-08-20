"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from src.pylib.pipeline import trait_list


class TestPart(unittest.TestCase):
    """Test the plant part parser."""

    def test_part_01(self):
        self.assertEqual(
            trait_list('with thick, woody rootstock.'),
            [{'woodiness': 'woody', 'trait': 'rootstock_woodiness',
              'start': 12, 'end': 17},
             {'part': 'rootstock', 'trait': 'part', 'start': 18, 'end': 27}]
        )

    def test_part_02(self):
        self.assertEqual(
            trait_list('leaflets mostly 1 or 3'),
            [{'part': 'leaflet', 'trait': 'part', 'start': 0, 'end': 8},
             {'low': 1, 'high': 3, 'trait': 'leaflet_count', 'start': 16,
              'end': 22}]
        )

    def test_part_03(self):
        self.assertEqual(
            trait_list('Receptacle discoid.'),
            []
        )
