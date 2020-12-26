"""Setup for all tests."""

from typing import Dict, List

from src.matchers.pipeline import Pipeline

TEST = Pipeline()  # Singleton for testing


def test(text: str) -> List[Dict]:
    """Find entities in the doc."""
    return TEST.test_traits(text)
