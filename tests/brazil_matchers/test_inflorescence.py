"""Test plant inflorescence trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten  # pylint: disable=import-error

from src.brazil_matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestMorphism(unittest.TestCase):
    """Test plant inflorescence trait matcher."""

    def test_inflorescence_01(self):
        self.assertEqual(
            NLP(shorten("""Inflorescence: raceme congested;""")),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 14},
             {'part': 'inflorescence', 'inflorescence': 'congested',
              'trait': 'inflorescence', 'start': 15, 'end': 31}]
        )

    def test_inflorescence_02(self):
        self.assertEqual(
            NLP(shorten("""Inflorescence: raceme lax;""")),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 14},
             {'part': 'inflorescence', 'inflorescence': 'lax',
              'trait': 'inflorescence', 'start': 15, 'end': 25}]
        )
