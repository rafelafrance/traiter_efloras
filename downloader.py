#!/usr/bin/env python

"""Build and run a wget command."""

import os
import sys
import time
import random
import argparse
import textwrap
import urllib.request
import regex
from lxml import html
from efloras.pylib import util
from efloras.pylib import family_util as futil


LINK = regex.compile(
    r'.*florataxon\.aspx\?flora_id=\d+&taxon_id=(?P<taxon_id>\d+)',
    regex.VERBOSE | regex.IGNORECASE)


def efloras(family_name, taxon_id, parents, flora_id):
    """Get a family of taxa from the efloras web site."""
    parents.add(taxon_id)

    taxon_dir = f'{family_name}_{flora_id}'
    path = util.DATA_DIR / taxon_dir / f'taxon_id_{taxon_id}.html'
    url = ('http://www.efloras.org/florataxon.aspx'
           f'?flora_id={flora_id}'
           f'&taxon_id={taxon_id}')

    print(f'Downloading: {url}')

    if not path.exists():
        urllib.request.urlretrieve(url, path)
        time.sleep(random.randint(10, 20))  # 15 sec +/- 5 sec

    with open(path) as in_file:
        page = html.fromstring(in_file.read())

    for link in page.xpath('//a'):
        href = link.attrib.get('href', '')
        match = LINK.match(href)
        if match and match.group('taxon_id') not in parents:
            efloras(family_name, match.group('taxon_id'), parents, flora_id)


def parse_args(flora_ids):
    """Process command-line arguments."""
    description = """Download data from the eFloras website."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--family', '-f', action='append',
        help="""Which family to download.""")

    arg_parser.add_argument(
        '--flora-id', '--id', '-F', type=int, default=1,
        choices=[k for k in flora_ids.keys()],
        help="""Which flora ID to download. Default 1.""")

    arg_parser.add_argument(
        '--list-flora-ids', '-l', action='store_true',
        help="""List flora IDs and exit.""")

    arg_parser.add_argument(
        '--search', '-s',
        help="""Search the families list for one that matches the string.
            The patterns will match either the family name or the flora name.
            You may use '*' and '?' wildcards for pattern matching.""")

    args = arg_parser.parse_args()

    if args.family:
        args.family = [x.lower() for x in args.family]
        for family in args.family:
            if (family, args.flora_id) not in FAMILIES:
                sys.exit(f'"{family}" is not in flora {args.flora_id}.')

    return args


def main(args, families, flora_ids):
    """Perform actions based on the arguments."""
    if args.list_flora_ids:
        futil.print_flora_ids(flora_ids)
        sys.exit()

    if args.search:
        futil.search_families(args, families)
        sys.exit()

    for family in args.family:
        key = (family, args.flora_id)
        family_name = FAMILIES[key]['family']
        taxon_id = FAMILIES[key]['taxon_id']
        dir_ = f'{family_name}_{args.flora_id}'
        os.makedirs(util.DATA_DIR / dir_, exist_ok=True)
        efloras(family_name, taxon_id, set(), args.flora_id)


if __name__ == "__main__":
    FAMILIES = futil.get_families()
    FLORA_IDS = futil.get_flora_ids()
    ARGS = parse_args(FLORA_IDS)
    main(ARGS, FAMILIES, FLORA_IDS)
