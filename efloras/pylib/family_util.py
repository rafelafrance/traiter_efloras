"""Common functions related to extracting families."""

import csv
from datetime import datetime
import regex
import efloras.pylib.util as util


EFLORAS_FAMILIES = util.DATA_DIR / 'eFloras_family_list.csv'


FLORA_ID = 1
LINK = ('www.efloras.org/florataxon.aspx?'
        rf'flora_id={FLORA_ID}&taxon_id=\1')


def get_families():
    """Get a list of all families in the eFloras North American catalog."""
    families = {}

    with open(EFLORAS_FAMILIES) as in_file:

        for family in csv.DictReader(in_file):

            times = {'created': '', 'modified': '', 'count': 0}

            path = util.DATA_DIR / f"{family['family']}_{family['flora_id']}"
            if path.exists():
                times['count'] = len(list(path.glob('**/*.html')))
                if times['count']:
                    stat = path.stat()
                    times['created'] = datetime.fromtimestamp(
                        stat.st_ctime).strftime('%Y-%m-%d %H:%M')
                    times['modified'] = datetime.fromtimestamp(
                        stat.st_mtime).strftime('%Y-%m-%d %H:%M')

            key = (family['family'].lower(), int(family['flora_id']))
            families[key] = {**family, **times}

    return families


def print_families(families):
    """Display a list of all families."""
    template = '{:<20} {:>8} {:>8} {:<30}  {:<20} {:<20} {:>8}'

    print(template.format(
        'Family',
        'Taxon Id',
        'Flora Id',
        'Flora Name',
        'Directory Created',
        'Directory Modified',
        'File Count'))

    for family in families.values():
        print(template.format(
            family['family'],
            family['taxon_id'],
            family['flora_id'],
            family['flora_name'],
            family['created'],
            family['modified'],
            family['count'] if family['count'] else ''))


def search_families(args, families):
    """Display a list of all families that match the given pattern."""
    template = '{:<20} {:>8} {:>8} {:<30}  {:<20} {:<20} {:>8}'

    pattern = args.search.replace('*', '.*').replace('?', '.?')
    pattern = regex.compile(pattern, regex.IGNORECASE)

    print(template.format(
        'Family',
        'Taxon Id',
        'Flora Id',
        'Flora Name',
        'Directory Created',
        'Directory Modified',
        'File Count'))

    for family in families.values():
        if (pattern.search(family['family'])
                or pattern.search(family['flora_name'])):
            print(template.format(
                family['family'],
                family['taxon_id'],
                family['flora_id'],
                family['flora_name'],
                family['created'],
                family['modified'],
                family['count'] if family['count'] else ''))


def get_flora_ids():
    """Get a list of flora IDs."""
    flora_ids = {}
    with open(EFLORAS_FAMILIES) as in_file:
        for family in csv.DictReader(in_file):
            flora_ids[int(family['flora_id'])] = family['flora_name']
    return flora_ids


def print_flora_ids(flora_ids):
    """Display a list of all flora IDs."""
    template = '{:>8}  {:<30}'

    print(template.format('Flora ID', 'Name'))

    for fid, name in flora_ids.items():
        print(template.format(fid, name))
