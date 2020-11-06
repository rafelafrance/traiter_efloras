"""Test plant shape trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from tests.setup import test_brazil


class TestShape(unittest.TestCase):
    """Test plant shape trait matcher."""

    def test_shape_01(self):
        self.assertEqual(
            test_brazil(shorten('form of the leaflet lanceolate;')),
            [{'shape': 'lanceolate', 'part': 'leaflet',
              'trait': 'shape', 'start': 0, 'end': 30}]
        )

    def test_shape_02(self):
        self.assertEqual(
            test_brazil(shorten("""
                form of the leaflet elliptic/obovate/rhombic;""")),
            [{'shape': ['elliptic', 'obovate', 'rhomboic'], 'part': 'leaflet',
              'trait': 'shape', 'start': 0, 'end': 44}]
        )

    def test_shape_03(self):
        self.assertEqual(
            test_brazil(shorten('nectary patelliform.')),
            [{'shape': 'patelliform', 'part': 'nectary',
              'trait': 'shape', 'start': 0, 'end': 19}]
        )
