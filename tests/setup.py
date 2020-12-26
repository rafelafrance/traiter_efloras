"""Setup for all tests."""

from typing import Dict, List

from src.matchers.pipeline import Pipeline as EflorasPipe

TEST = EflorasPipe()  # Singleton for testing


def test_efloras(text: str) -> List[Dict]:
    """Find entities in the doc."""
    return TEST.test_traits(text)
