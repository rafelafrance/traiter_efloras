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


# Don't hit the site too hard
SLEEP_MID = 20
SLEEP_RADIUS = 5
SLEEP_RANGE = (SLEEP_MID - SLEEP_RADIUS, SLEEP_MID + SLEEP_RADIUS)


def efloras(family_name, flora_id, taxon_id, parents):
    """Get a family of taxa from the efloras web site."""
    # http://www.efloras.org/florataxon.aspx?flora_id=1&taxon_id=10041
    lower_link = regex.compile(
        r'.*florataxon\.aspx\?flora_id=\d+&taxon_id=(?P<taxon_id>\d+)',
        regex.VERBOSE | regex.IGNORECASE)

    parents.add(taxon_id)

    taxon_dir = f'{family_name}_{flora_id}'
    path = util.DATA_DIR / taxon_dir / f'taxon_id_{taxon_id}.html'
    url = ('http://www.efloras.org/florataxon.aspx'
           f'?flora_id={flora_id}'
           f'&taxon_id={taxon_id}')

    print(f'Downloading: {url}')

    if not path.exists():
        urllib.request.urlretrieve(url, path)
        time.sleep(random.randint(SLEEP_RANGE[0], SLEEP_RANGE[1]))

    with open(path) as in_file:
        page = html.fromstring(in_file.read())

    for link in page.xpath('//a'):
        href = link.attrib.get('href', '')
        match = lower_link.match(href)
        if match and match.group('taxon_id') not in parents:
            efloras(family_name, flora_id, match.group('taxon_id'), parents)


def family_tree(family_name, flora_id, taxon_id, parents):
    """Get to the pages via the family links."""
    # http://www.efloras.org/browse.aspx?flora_id=1&page=2
    page_link = regex.compile(
        (r'browse\.aspx\?flora_id=\d+&start_taxon_id=(?P<taxon_id>\d+)'
         r'&page=(?P<page>\d+)'),
        regex.VERBOSE | regex.IGNORECASE)

    parents.add(taxon_id)

    page = tree_page(family_name, flora_id, taxon_id, parents)

    for anchor in page.xpath('//a'):
        href = anchor.attrib.get('href', '')
        match = page_link.search(href)
        if match:
            page_no = int(match.group('page'))
            name = f'{taxon_id}_{page_no}'
            if name not in parents:
                parents.add(name)
                tree_page(
                    family_name, flora_id, taxon_id, parents, page_no=page_no)


def tree_page(family_name, flora_id, taxon_id, parents, page_no=1):
    """Get a family tree page."""
    lower_link = regex.compile(
        r'browse\.aspx\?flora_id=\d+&start_taxon_id=(?P<taxon_id>\d+)',
        regex.VERBOSE | regex.IGNORECASE)

    taxon_dir = f'tree_{family_name}_{flora_id}'
    path = util.DATA_DIR / taxon_dir / f'taxon_id_{taxon_id}.html'
    if page_no > 1:
        page_name = f'taxon_id_{taxon_id}_{page_no}.html'
        path = util.DATA_DIR / taxon_dir / page_name

    url = ('http://www.efloras.org/browse.aspx'
           f'?flora_id={flora_id}'
           f'&start_taxon_id={taxon_id}')
    if page_no > 1:
        url += f'&page={page_no}'

    print(f'Downloading: {url}')

    if not path.exists():
        urllib.request.urlretrieve(url, path)
        time.sleep(random.randint(SLEEP_RANGE[0], SLEEP_RANGE[1]))

    with open(path) as in_file:
        page = html.fromstring(in_file.read())

    for link in page.xpath('//a'):
        href = link.attrib.get('href', '')
        match = lower_link.search(href)
        if match and match.group('taxon_id') not in parents:
            family_tree(
                family_name, flora_id, match.group('taxon_id'), parents)

    return page


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
        '--family-tree', '-t', action='store_true',
        help="""Get the family tree.""")

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
        if args.family_tree:
            dir_ = f'tree_{family_name}_{args.flora_id}'
            os.makedirs(util.DATA_DIR / dir_, exist_ok=True)
            family_tree(family_name, args.flora_id, taxon_id, set())
        else:
            dir_ = f'{family_name}_{args.flora_id}'
            os.makedirs(util.DATA_DIR / dir_, exist_ok=True)
            efloras(family_name, args.flora_id, taxon_id, set())


if __name__ == "__main__":
    FAMILIES = futil.get_families()
    FLORA_IDS = futil.get_flora_ids()
    ARGS = parse_args(FLORA_IDS)
    main(ARGS, FAMILIES, FLORA_IDS)
