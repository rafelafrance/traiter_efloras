"""Misc. utils."""

from pathlib import Path

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find('efloras') > -1 else Path.cwd().parent

DATA_DIR = BASE_DIR / 'data'
VOCAB_DIR = BASE_DIR / 'src' / 'vocabulary'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
ATTACH_STEP = 'attach'

CONVERT = {
    'cm': 10.0,
    'dm': 100.0,
    'm': 1000.0,
    'mm': 1.0,
    'µm': 1.0e-3,
}


def convert(number, units):
    """Normalize the units to meters."""
    return number * CONVERT.get(units, 1.0)
