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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from traiter.pylib.util import log

from src.pylib.brazil_util import BRAZIL_DIR, BRAZIL_FAMILIES, SITE, \
    species_path

# Don't hit the site too hard
SLEEP_MID = 15
SLEEP_RADIUS = 5
SLEEP_RANGE = (SLEEP_MID - SLEEP_RADIUS, SLEEP_MID + SLEEP_RADIUS)

WAIT = 20  # How many seconds to wait for the page action to happen

# Set a timeout for requests
TIMEOUT = 60
socket.setdefaulttimeout(TIMEOUT)


def main(args):
    """Download the data."""
    if args.all_families:
        all_families()
        sys.exit()

    if not args.family_action:
        log('Error: You must choose a --family-action.')
        sys.exit()

    if args.family_action == 'list':
        species(args)
    elif args.family_action == 'pages':
        pages(args)


def all_families():
    """Save a list of families."""
    url = SITE + 'families'
    urllib.request.urlretrieve(url, BRAZIL_FAMILIES)


def species(args):
    """Download all species for a family."""
    url = SITE + f'species/{args.family}'
    urllib.request.urlretrieve(url, species_path(args.family))


def pages(args):
    """Download all treatment pages for a family."""
    driver = webdriver.Firefox(log_path=args.log_file)
    driver.implicitly_wait(2)

    path = species_path(args.family)

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

    first_time = True

    for _, row in df.iterrows():
        name = f"{row['genus']}_{row['specificepithet']}"
        if row['infraspecificepithet']:
            name += f"_{row['infraspecificepithet']}"
        name += '.html'

        path = dir_ / name

        log(f'Downloading: {name}')

        # Don't hit the site too hard
        if not first_time:
            time.sleep(random.randint(SLEEP_RANGE[0], SLEEP_RANGE[1]))
        first_time = False

        url = row['references'] + '&lingua=en'
        download_page(driver, url, path)

    driver.close()


def download_page(driver, url, path):
    """Download a page if it does not exist."""
    if path.exists():
        return

    driver.get(url)

    spinner = 'modalTelaCarregando'
    try:
        WebDriverWait(driver, WAIT).until(
            ec.invisibility_of_element((By.ID, spinner)))
    except (TimeoutError, socket.timeout, HTTPError):
        log(f'Error: waiting for {spinner} to stop')
        return

    spinner = 'linkCites'
    try:
        WebDriverWait(driver, WAIT).until(
            ec.invisibility_of_element((By.ID, spinner)))
    except (TimeoutError, socket.timeout, HTTPError):
        log(f'Error: waiting for {spinner} to stop')
        return

    with open(path, 'w') as out_file:
        out_file.write(driver.page_source)


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

    arg_parser.add_argument(
        '--log-file', '-l', default='geckodriver.log',
        help="""Path to the selenium driver log file.""")

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
