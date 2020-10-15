"""Test plant shape trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from src.brazil_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestShape(unittest.TestCase):
    """Test plant shape trait matcher."""

    def test_shape_01(self):
        self.assertEqual(
            NLP(shorten('form of the leaflet lanceolate;')),
            [{'shape': 'lanceolate', 'part': 'leaflet',
              'trait': 'shape', 'start': 0, 'end': 30}]
        )

    def test_shape_02(self):
        self.assertEqual(
            NLP(shorten('form of the leaflet elliptic/obovate/rhombic;')),
            [{'shape': ['elliptic', 'obovate', 'rhomboic'], 'part': 'leaflet',
              'trait': 'shape', 'start': 0, 'end': 44}]
        )

    def test_shape_03(self):
        self.assertEqual(
            NLP(shorten('nectary patelliform.')),
            [{'shape': 'patelliform', 'part': 'nectary',
              'trait': 'shape', 'start': 0, 'end': 19}]
        )
