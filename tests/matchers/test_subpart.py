"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from src.pylib.pipeline import PIPELINE

NLP = PIPELINE.trait_list


class TestSubpart(unittest.TestCase):
    """Test the plant subpart parser."""

    def test_subpart_01(self):
        self.assertEqual(
            NLP('terminal lobe ovate-trullate,'),
            [{'location': 'terminal', 'subpart': 'lobe',
              'trait': 'subpart', 'start': 0, 'end': 13},
             {'shape': 'ovate-trullate', 'location': 'terminal',
              'trait': 'plant_lobe_shape', 'start': 14, 'end': 28}]
        )
