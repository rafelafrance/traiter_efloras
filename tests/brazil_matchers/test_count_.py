"""Test plant count trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

# from traiter.pylib.util import shorten  # pylint: disable=import-error

from src.brazil_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestCount(unittest.TestCase):
    """Test plant count trait matcher."""

    def test_count_01(self):
        self.assertEqual(
            NLP('Leaf: number of the pairs of the leaflet 1/2/3;'),
            [{'low': 1, 'high': 3,
              'trait': 'count', 'per_count': 'pairs',
              'start': 41, 'end': 46}]
        )
