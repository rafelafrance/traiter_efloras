"""Test attaching traits to plant parts."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.util import shorten

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestAttach(unittest.TestCase):
    """Test attaching traits to plant parts."""

    def test_attach_01(self):
        self.assertEqual(
            MATCHER.parse(shorten("""leaves and yellow petals.""")),
            {'part': [{'start': 0, 'end': 6, 'part': 'leaf'},
                      {'start': 18, 'end': 24, 'part': 'petal'}],
             'petal_color': [{'color': 'yellow', 'start': 11, 'end': 17}]}
        )
