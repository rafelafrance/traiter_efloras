"""Misc. utils."""
import csv
import re
from datetime import datetime

from efloras.patterns.shape import MULTIPLE_DASHES
from efloras.pylib.const import DATA_DIR, EFLORAS_FAMILIES, REPLACE

CONVERT = {
    'cm': 10.0,
    'dm': 100.0,
    'm': 1000.0,
    'mm': 1.0,
    'µm': 1.0e-3,
    'centimeters': 10.0,
    'decimeters': 100.0,
    'meters': 1000.0,
    'millimeters': 1.0,
}


def convert(number, units):
    """Normalize the units to meters."""
    return number * CONVERT.get(units, 1.0)


def get_families():
    """Get a list of all families in the eFloras catalog."""
    families = {}

    with open(EFLORAS_FAMILIES) as in_file:

        for family in csv.DictReader(in_file):

            times = {'created': '', 'modified': '', 'count': 0}

            path = (DATA_DIR / 'eFloras'
                    / f"{family['family']}_{family['flora_id']}")

            if path.exists():
                times['count'] = len(list(path.glob('**/treatments/*.html')))
                if times['count']:
                    stat = path.stat()
                    times['created'] = datetime.fromtimestamp(
                        stat.st_ctime).strftime('%Y-%m-%d %H:%M')
                    times['modified'] = datetime.fromtimestamp(
                        stat.st_mtime).strftime('%Y-%m-%d %H:%M')

            key = (family['family'].lower(), int(family['flora_id']))
            families[key] = {**family, **times}

    return families


def get_flora_ids():
    """Get a list of flora IDs."""
    flora_ids = {}
    with open(EFLORAS_FAMILIES) as in_file:
        for family in csv.DictReader(in_file):
            flora_ids[int(family['flora_id'])] = family['flora_name']
    return flora_ids
