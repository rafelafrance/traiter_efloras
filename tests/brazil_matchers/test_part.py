"""Test plant part trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from src.brazil_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestPart(unittest.TestCase):
    """Test plant shape trait matcher."""

    def test_part_01(self):
        self.assertEqual(
            NLP(shorten('Leaf: number of the pairs')),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5}]
        )
