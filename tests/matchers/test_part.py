"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.pylib.pipeline import parse


class TestPart(unittest.TestCase):
    """Test the plant part parser."""

    def test_part_01(self):
        self.assertEqual(
            parse('with thick, woody rootstock.'),
            {'rootstock_woodiness': [
                {'start': 12, 'end': 17, 'woodiness': 'woody'}],
             'part': [{'start': 18, 'end': 27, 'part': 'rootstock'}]}
        )

    def test_part_02(self):
        self.assertEqual(
            parse('leaf­lets mostly 1 or 3'),
            {'part': [{'part': 'leaflet', 'start': 0, 'end': 9}],
             'leaflet_count': [{'low': 1, 'high': 3, 'start': 17, 'end': 23}]}
        )

    def test_part_03(self):
        self.assertEqual(
            parse('Receptacle discoid.'),
            {}
        )
