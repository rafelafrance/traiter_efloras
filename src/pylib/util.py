"""Misc. utils."""
import csv
from datetime import datetime

from src.pylib.consts import CONVERT, DATA_DIR, EFLORAS_FAMILIES


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
