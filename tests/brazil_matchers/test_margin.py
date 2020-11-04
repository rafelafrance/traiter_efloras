"""Test plant margin trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from src.brazil_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestMargin(unittest.TestCase):
    """Test plant margin trait matcher."""

    def test_margin_01(self):
        self.assertEqual(
            NLP(shorten("""
                Fruit: margin smooth or sinuose the irregularly constricted.
                """)),
            [{'part': 'fruit', 'trait': 'part', 'start': 0, 'end': 6},
             {'subpart': 'margin',
              'margin': ['smooth', 'sinuose', 'irregularly constricted'],
              'trait': 'margin', 'start': 7, 'end': 59}]
        )

    def test_margin_02(self):
        self.assertEqual(
            NLP(shorten("""Fruit: margin moniliform.""")),
            [{'part': 'fruit', 'trait': 'part', 'start': 0, 'end': 6},
             {'subpart': 'margin', 'margin': 'moniliform',
              'trait': 'margin', 'start': 7, 'end': 24}]
        )
