"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from tests.setup import test


class TestSubpart(unittest.TestCase):
    """Test the plant subpart parser."""

    def test_subpart_01(self):
        self.assertEqual(
            test('terminal lobe ovate-trullate,'),
            [{'location': 'terminal', 'subpart': 'lobe',
              'trait': 'subpart', 'start': 0, 'end': 13},
             {'shape': 'ovate-trullate',
              'trait': 'shape', 'part': 'plant', 'subpart': 'lobe',
              'start': 14, 'end': 28}]
        )
