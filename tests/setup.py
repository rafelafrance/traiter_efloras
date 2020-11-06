"""Setup for all tests."""

from typing import Dict, List

from src.brazil_matchers.pipeline import Pipeline as BrazilPipe
from src.efloras_matchers.pipeline import Pipeline as EflorasPipe

TEST_BRAZIL = BrazilPipe()  # Singleton for testing
TEST_EFLORAS = EflorasPipe()  # Singleton for testing


def test_brazil(text: str) -> List[Dict]:
    """Find entities in the doc."""
    return TEST_BRAZIL.test_traits(text)


def test_efloras(text: str) -> List[Dict]:
    """Find entities in the doc."""
    return TEST_EFLORAS.test_traits(text)
