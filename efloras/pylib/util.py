"""Holds misc functions and constants."""

import csv
from pathlib import Path
from datetime import datetime
import regex
import inflect

FLAGS = regex.VERBOSE | regex.IGNORECASE

BATCH_SIZE = 1_000_000  # How many records to work with at a time

RAW_DIR = Path('.') / 'data'
EFLORAS_NA_FAMILIES = RAW_DIR / 'eFloras_family_list.csv'

INFLECT = inflect.engine()


class DotDict(dict):
    """Allow dot.notation access to dictionary items"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def shorten(text):
    """Collapse whitespace in a string."""
    return ' '.join(text.split())


def squash(values):
    """Squash a list to a single value is its length is one."""
    return values if len(values) != 1 else values[0]


def as_list(values):
    """Convert values to a list."""
    return values if isinstance(values, (list, tuple, set)) else [values]


def as_tuple(values):
    """Convert values to a tuple."""
    return values if isinstance(values, tuple) else tuple(values)


def ordinal(i):
    """Convert the digit to an ordinal value: 1->1st, 2->2nd, etc."""
    return INFLECT.ordinal(i)


def number_to_words(number):
    """Convert the number or ordinal value into words."""
    return INFLECT.number_to_words(number)


def camel_to_snake(name):
    """Convert a camel case string to snake case."""
    split = regex.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return regex.sub('([a-z0-9])([A-Z])', r'\1_\2', split).lower()


def get_families():
    """Get a list of all families in the eFloras North American catalog."""
    families = {}

    with open(EFLORAS_NA_FAMILIES) as in_file:

        for family in csv.DictReader(in_file):

            times = {'created': '', 'modified': '', 'count': 0}

            path = RAW_DIR / family['Name']
            if path.exists():
                times['count'] = len(list(path.glob('**/*.html')))
                if times['count']:
                    stat = path.stat()
                    times['created'] = datetime.fromtimestamp(
                        stat.st_ctime).strftime('%Y-%m-%d %H:%M')
                    times['modified'] = datetime.fromtimestamp(
                        stat.st_mtime).strftime('%Y-%m-%d %H:%M')

            families[family['Name'].lower()] = {
                'name': family['Name'],
                'taxon_id': family['Taxon Id'],
                'lower_taxa': family['# Lower Taxa'],
                'volume': family['Volume'],
                'created': times['created'],
                'modified': times['modified'],
                'count': times['count'],
                }

    return families


def print_families(families):
    """Display a list of all families."""
    template = '{:<20} {:>10}  {:<25}  {:<20}  {:<20} {:>10}'

    print(template.format(
        'Family',
        'Taxon Id',
        'Volume',
        'Directory Created',
        'Directory Modified',
        'File Count'))

    for family in families.values():
        print(template.format(
            family['name'],
            family['taxon_id'],
            family['volume'],
            family['created'],
            family['modified'],
            family['count'] if family['count'] else ''))


def to_float(value):
    """Convert the value to a float."""
    value = regex.sub(r'[^\d.]', '', value) if value else ''
    try:
        return float(value)
    except ValueError:
        return None
