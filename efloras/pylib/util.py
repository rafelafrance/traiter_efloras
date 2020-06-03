"""Misc. utils."""

from pathlib import Path

DATA_DIR = Path('.') / 'data'
VOCAB_DIR = Path('.') / 'efloras' / 'vocabulary'


CONVERT = {
    'cm': 10.0,
    'm': 1000.0,
    'mm': 1.0,
    'µm': 1.0e-3,
}


def convert(number, units):
    """Normalize the units to meters."""
    return number * CONVERT.get(units, 1.0)
