"""Test plant count trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from tests.setup import test_brazil


class TestCount(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_count_01(self):
        self.assertEqual(
            test_brazil(shorten("""
                Leaf: number of the pairs of the leaflet 1/2/3;""")),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'low': 1, 'high': 3, 'per_count': 'pairs', 'part': 'leaflet',
              'trait': 'count', 'start': 6, 'end': 46}]
        )

    def test_count_02(self):
        self.assertEqual(
            test_brazil(shorten("""
                Leaf: number of the pairs of the leaflet 1/2/3 or more;
                """)),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5},
             {'low': 1, 'high': 3, 'more': True, 'per_count': 'pairs',
              'part': 'leaflet', 'trait': 'count', 'start': 6, 'end': 54}]
        )
