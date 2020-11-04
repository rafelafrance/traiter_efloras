"""Common utility functions for Brazil Flora"""

import json
from datetime import datetime

from src.pylib.util import DATA_DIR

BRAZIL_DIR = DATA_DIR / 'brazil'
BRAZIL_FAMILIES = BRAZIL_DIR / 'families.json'

SITE = 'http://servicos.jbrj.gov.br/flora/'


def get_families():
    """Get a list of all families in the Brazil catalog."""
    with open(BRAZIL_FAMILIES) as in_file:
        all_families = json.load(in_file)

    all_families = [f for f in all_families['result'] if f]

    families = {}

    for family in all_families:
        row = {'family': family, 'created': '', 'modified': '', 'count': 0}

        path = BRAZIL_DIR / family

        if path.exists():
            row['count'] = len(list(path.glob('*.html')))
            if row['count']:
                stat = path.stat()
                row['created'] = datetime.fromtimestamp(
                    stat.st_ctime).strftime('%Y-%m-%d %H:%M')
                row['modified'] = datetime.fromtimestamp(
                    stat.st_mtime).strftime('%Y-%m-%d %H:%M')

        families[family] = row

    return families


def print_families(families):
    """Display a list of all families."""
    template = '{:<20} {:<20} {:<20} {:>8}'

    print(template.format(
        'Family',
        'Directory Created',
        'Directory Modified',
        'Treatments'))

    for family in families.values():
        print(template.format(
            family['family'],
            family['created'],
            family['modified'],
            family['count'] if family['count'] else ''))


def species_path(family):
    """Build the path to the list of species for the family."""
    return BRAZIL_DIR / f'{family.capitalize()}_species.json'
