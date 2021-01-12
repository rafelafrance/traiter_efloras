"""Setup for all tests."""

from typing import Dict, List

from traiter.util import shorten  # pylint: disable=import-error

from src.matchers.pipeline import Pipeline

TEST = Pipeline()  # Singleton for testing


def test(text: str) -> List[Dict]:
    """Find entities in the doc."""
    text = shorten(text)
    return TEST.test_traits(text)
