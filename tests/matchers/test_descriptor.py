"""Test the plant descriptor matcher."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.matchers.matcher import Matcher

MATCHER = Matcher()


class TestDescriptor(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_descriptor_01(self):
        self.assertEqual(
            MATCHER.parse(
                'bisexual (unisexual and plants sometimes gynodioecious, '
                'or plants dioecious'),
            {
                'plant_reproduction': [
                    {'value': 'bisexual', 'start': 0, 'end': 8},
                    {'value': 'unisexual', 'start': 10, 'end': 19},
                    {'value': 'gynodioecious', 'start': 41, 'end': 54},
                    {'value': 'dioecious', 'start': 66, 'end': 75}],
                'part': [
                    {'start': 24, 'end': 30, 'value': 'plant'},
                    {'start': 59, 'end': 65, 'value': 'plant'}]}
        )
