#!/usr/bin/env python

"""Build and run a wget command."""

import argparse
from html import unescape
import os
import random
import sys
import textwrap
import time
import urllib.request

import regex
# import pandas as pd
from bs4 import BeautifulSoup
from lxml import html

import efloras.pylib.util as util
from efloras.pylib import family_util as futil

# Don't hit the site too hard
SLEEP_MID = 15
SLEEP_RADIUS = 5
SLEEP_RANGE = (SLEEP_MID - SLEEP_RADIUS, SLEEP_MID + SLEEP_RADIUS)


def main(args, families, flora_ids):
    """Perform actions based on the arguments."""
    if args.list_flora_ids:
        futil.print_flora_ids(flora_ids)
        sys.exit()

    if args.search:
        futil.search_families(args, families)
        sys.exit()

    if args.update_families:
        update_families()
        sys.exit()

    for family in args.family:
        key = (family, args.flora_id)
        family_name = FAMILIES[key]['family']
        taxon_id = FAMILIES[key]['taxon_id']

        dir_ = futil.tree_dir(args.flora_id, family_name)
        os.makedirs(dir_, exist_ok=True)

        dir_ = futil.treatment_dir(args.flora_id, family_name)
        os.makedirs(dir_, exist_ok=True)

        download(family_name, args.flora_id, taxon_id)


def update_families():
    """Update the list of families for each flora ID."""
    floras = get_floras()
    # for flora in floras:
    #     print(flora)
    #     get_families(flora['flora_id'])

    for flora in floras:
        pattern = f'flora_id={flora["flora_id"]}_page=*'
        families = []
        for page in sorted(util.FAMILY_DIR.glob(pattern)):
            print(page)


def get_families(flora_id):
    """Get the families for the flora."""
    base_url = f'{futil.CITE}/browse.aspx?flora_id={flora_id}'
    path = util.FAMILY_DIR / f'flora_id={flora_id}_page=1.html'
    urllib.request.urlretrieve(base_url, path)  # ##########################

    with open(path) as in_file:
        page = in_file.read()
    soup = BeautifulSoup(page, features='lxml')
    link_re = regex.compile(fr'browse.aspx\?flora_id={flora_id}&page=\d+')
    page_re = regex.compile(r'page=(\d)')

    pages = set()

    for link in soup.findAll('a', attrs={'href': link_re}):
        page_no = page_re.search(str(link))
        page_no = int(page_no[1])
        pages.add(page_no)

    for page in pages:
        url = base_url + f'&page={page}'
        path = util.FAMILY_DIR / f'flora_id={flora_id}_page={page}.html'
        urllib.request.urlretrieve(url, path)


def get_floras():
    """Get the floras from the main page."""
    url = futil.CITE
    path = util.FAMILY_DIR / 'home_page.html'
    # urllib.request.urlretrieve(url, path)  # ###############################

    with open(path) as in_file:
        page = in_file.read()

    floras = []

    soup = BeautifulSoup(page, features='lxml')
    floras_re = regex.compile(r'flora_page.aspx\?flora_id=(\d+)')

    for link in soup.findAll('a', attrs={'href': floras_re}):
        flora_id = floras_re.search(str(link))
        floras.append({
            'flora_id': int(flora_id[1]),
            'flora_name': link.text,
        })

    return sorted(floras, key=lambda x: x['flora_id'])


def download(family_name, flora_id, taxon_id):
    """Download the family tree and then treatments."""
    family_tree(family_name, flora_id, taxon_id, set())

    tree_dir = futil.tree_dir(flora_id, family_name)
    for path in tree_dir.glob('*.html'):
        with open(path) as in_file:
            page = html.fromstring(in_file.read())
        get_treatments(flora_id, family_name, page)


def get_treatments(flora_id, family_name, page):
    """Get the treatment files in the tree."""
    treatement = regex.compile(
        r'.*florataxon\.aspx\?flora_id=\d+&taxon_id=(?P<taxon_id>\d+)',
        regex.VERBOSE | regex.IGNORECASE)

    for anchor in page.iterlinks():
        link = anchor[2]
        if match := treatement.match(link):
            taxon_id = match.group('taxon_id')
            get_treatment(flora_id, family_name, taxon_id)


def get_treatment(flora_id, family_name, taxon_id):
    """Get one treatment file in the tree."""
    path = futil.treatment_file(flora_id, family_name, taxon_id)
    url = (f'{futil.CITE}/florataxon.aspx'
           f'?flora_id={flora_id}'
           f'&taxon_id={taxon_id}')

    print(f'Treatment: {url}')

    if not path.exists():
        urllib.request.urlretrieve(url, path)
        time.sleep(random.randint(SLEEP_RANGE[0], SLEEP_RANGE[1]))


def family_tree(family_name, flora_id, taxon_id, parents):
    """Get to the pages via the family links."""
    # http://www.efloras.org/browse.aspx?flora_id=1&page=2
    page_link = regex.compile(
        (r'browse\.aspx\?flora_id=\d+'
         r'&start_taxon_id=(?P<taxon_id>\d+)'
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

    path = futil.tree_file(flora_id, family_name, taxon_id, page_no)

    url = (f'{futil.CITE}/browse.aspx'
           f'?flora_id={flora_id}'
           f'&start_taxon_id={taxon_id}')
    if page_no > 1:
        url += f'&page={page_no}'

    print(f'Tree: {url}')

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
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--update-families', '-u', action='store_true',
        help="""Download the list of families for each flora ID.""")

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


if __name__ == "__main__":
    FAMILIES = futil.get_families()
    FLORA_IDS = futil.get_flora_ids()
    ARGS = parse_args(FLORA_IDS)
    main(ARGS, FAMILIES, FLORA_IDS)
