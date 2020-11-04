"""Test plant surface trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from src.brazil_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestSurface(unittest.TestCase):
    """Test plant surface trait matcher."""

    def test_surface_01(self):
        self.assertEqual(
            NLP(shorten("""
                indumentum of the leaflet villose on the surface abaxial;
                """)),
            [{'surface': 'villose', 'location': 'abaxial',
              'part': 'leaflet', 'subpart': 'indumentum',
              'trait': 'surface', 'start': 0, 'end': 56}]
        )

    def test_surface_02(self):
        self.assertEqual(
            NLP(shorten("""
                Flower: indumentum of the calyx present;
                indumentum of the corolla absent.
                """)),
            [{'part': 'flower', 'trait': 'part', 'start': 0, 'end': 7},
             {'part': 'calyx', 'subpart': 'indumentum', 'present': True,
              'trait': 'surface', 'start': 8, 'end': 39},
             {'part': 'corolla', 'subpart': 'indumentum', 'present': False,
              'trait': 'surface', 'start': 41, 'end': 73}
             ]
        )

    def test_surface_03(self):
        self.assertEqual(
            NLP(shorten("""
                indumentum of the calyx absent/present;
                """)),
            [{'part': 'calyx', 'subpart': 'indumentum',
              'present': [False, True],
              'trait': 'surface', 'start': 0, 'end': 38}
             ]
        )

    def test_surface_04(self):
        self.assertEqual(
            NLP(shorten("""
                indumentum of the leaflet puberulent on the surface abaxial;
                """)),
            [{'surface': 'puberulent', 'part': 'leaflet',
              'subpart': 'indumentum', 'location': 'abaxial',
              'trait': 'surface', 'start': 0, 'end': 59}]
        )

    def test_surface_05(self):
        self.assertEqual(
            NLP(shorten("""indumentum of the leaflet glabrous;""")),
            [{'surface': 'glabrous', 'part': 'leaflet',
              'subpart': 'indumentum',
              'trait': 'surface', 'start': 0, 'end': 34}]
        )
