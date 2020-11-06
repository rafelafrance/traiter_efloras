"""Test plant part trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from tests.setup import test_brazil


class TestPart(unittest.TestCase):
    """Test plant shape trait matcher."""

    def test_part_01(self):
        self.assertEqual(
            test_brazil(shorten('Leaf: number of the pairs')),
            [{'part': 'leaf', 'trait': 'part', 'start': 0, 'end': 5}]
        )
