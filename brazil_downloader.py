#!/usr/bin/env python

"""Download files from Brazilian Flora 2020 Web Service."""

import argparse
import json
import os
import random
import socket
import sys
import textwrap
import time
import urllib.request
from urllib.error import HTTPError

import pandas as pd

from src.pylib.util import DATA_DIR

# Don't hit the site too hard
SLEEP_MID = 15
SLEEP_RADIUS = 5
SLEEP_RANGE = (SLEEP_MID - SLEEP_RADIUS, SLEEP_MID + SLEEP_RADIUS)

# Make a few attempts to download a page
ERROR_SLEEP = 120
ERROR_RETRY = 10

# Set a timeout for requests
TIMEOUT = 30
socket.setdefaulttimeout(TIMEOUT)

BRAZIL_DIR = DATA_DIR / 'brazil'

SITE = 'http://servicos.jbrj.gov.br/flora/'


def main(args):
    """Download the pages."""
    if args.all_families:
        families()
        sys.exit()

    if not args.family_action:
        print('You must choose a --family-action.')
        sys.exit()

    if args.family_action == 'list':
        species(args)
    elif args.family_action == 'pages':
        pages(args)


def families():
    """Save a list of families."""
    url = SITE + 'families'
    path = BRAZIL_DIR / 'families.json'
    urllib.request.urlretrieve(url, path)


def species(args):
    """Download all species for a family."""
    url = SITE + f'species/{args.family_species}'
    urllib.request.urlretrieve(url, species_path(args))


def pages(args):
    """Download all treatment pages for a family."""
    path = species_path(args)

    if not path.exists():
        sys.exit(f'The file {path} does not exist.')

    with open(path) as json_file:
        data = json.load(json_file)

    df = pd.DataFrame(data['result'])
    df = df.loc[df['taxonomicstatus'] == 'NOME_ACEITO']
    if args.filter:
        df['filter'] = df['scientificname'].str.lower()
        df = df.loc[df['filter'].str.contains(args.filter.lower())]

    dir_ = BRAZIL_DIR / args.family.capitalize()
    os.makedirs(dir_, exist_ok=True)

    for _, row in df.iterrows():
        name = f"{row['genus']}_{row['specificepithet']}"
        if row['infraspecificepithet']:
            name += f"_{row['infraspecificepithet']}"
        name += '.html'

        path = dir_ / name

        print(f'Downloading: {name}')
        if path.exists():
            continue

        url = row['references'] + '&lingua=en'
        download_page(url, path)
        return


def download_page(url, path):
    """Download a page if it does not exist."""
    if path.exists():
        return

    for attempt in range(ERROR_RETRY):
        if attempt > 0:
            print(f'Attempt {attempt + 1}')
        try:
            urllib.request.urlretrieve(url, path)
            time.sleep(random.randint(SLEEP_RANGE[0], SLEEP_RANGE[1]))
            break
        except (TimeoutError, socket.timeout, HTTPError):
            pass


def species_path(args):
    """Build the path to the list of species for the family."""
    return BRAZIL_DIR / f'{args.family.capitalize()}_species.json'


def parse_args():
    """Process command-line arguments."""
    description = """Download data from the Brazilian Flora web service."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--all-families', '-A', action='store_true',
        help="""Download a list of all families.""")

    arg_parser.add_argument(
        '--family', '-f',
        help="""The family.""")

    arg_parser.add_argument(
        '--family-action', '-a', choices=['list', 'pages'],
        help="""What are we doing with the family. Downloading a list of
            species for the family or downloading the species description
            pages for the family. You must download the list before the
            pages.""")

    arg_parser.add_argument(
        '--filter', '-F',
        help="""Filter the list of species in a family to include this string
            in the scientific name. E.g. 'Abarema' will get all species in the
            genus 'Abarema'.""")

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
