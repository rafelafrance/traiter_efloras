#!/usr/bin/env python3
"""Parse efloras treatments."""

import argparse
import sys
import textwrap
from copy import deepcopy

import efloras.pylib.util as util
from efloras.pylib.pipeline import pipeline
from efloras.pylib.util import get_family_flora_ids
from efloras.readers.efloras import efloras_reader
from efloras.writers.csv_ import csv_writer
from efloras.writers.data import biluo_writer, iob_writer, ner_writer
from efloras.writers.duck_db import duck_db
from efloras.writers.html_ import html_writer
from efloras.writers.sqlite3_db import sqlite3_db


def main(args):
    """Perform actions based on the arguments."""
    nlp = pipeline()

    families = get_efloras_families(args)

    rows = efloras_reader(args, families)

    for row in rows:
        row['doc'] = nlp(row['text'])

    if args.csv_file:
        copied = deepcopy(rows)
        csv_writer(args, copied)

    if args.html_file:
        copied = deepcopy(rows)
        html_writer(args, copied)

    if args.ner_file:
        copied = deepcopy(rows)
        ner_writer(args, copied)

    if args.iob_file:
        copied = deepcopy(rows)
        iob_writer(args, copied)

    if args.biluo_file:
        copied = deepcopy(rows)
        biluo_writer(args, copied)

    if args.sqlite3:
        copied = deepcopy(rows)
        sqlite3_db(args, copied)

    if args.duckdb:
        copied = deepcopy(rows)
        duck_db(args, copied)


def get_efloras_families(args):
    """Handle eFloras extractions"""
    families = {k: v for k, v in util.get_families().items() if
                v['count']}

    if not check_family_flora_ids(args, families):
        sys.exit(1)

    if args.list_families:
        print_families(families)
        sys.exit()

    return families


def check_family_flora_ids(args, families):
    """Validate family and flora ID combinations."""
    combos = get_family_flora_ids(args, families)

    flora = {i: False for i in args.flora_id}
    fams = {f: False for f in args.family}
    for combo in combos:
        fams[combo[0]] = True
        flora[combo[1]] = True

    ok = True
    for fam, hit in fams.items():
        if not hit:
            ok = False
            print(f'Family "{fam}" is not being used.')

    for id_, hit in flora.items():
        if not hit:
            ok = False
            print(f'Flora ID "{id_}" is not being used.')

    return ok


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
        'Treatments'))

    for family in families.values():
        print(template.format(
            family['family'],
            family['taxon_id'],
            family['flora_id'],
            family['flora_name'],
            family['created'],
            family['modified'],
            family['count'] if family['count'] else ''))


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from flora website."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--family', '-f', action='append',
        help="""Which family to extract.""")

    arg_parser.add_argument(
        '--genus', '-g', action='append',
        help="""Which genus to extract with in the family. Default is
            to select all genera. Although this is designed for selecting
            genera this is really just a filter on the taxa names so you
            can put in anything that matches a taxon name.""")

    flora_ids = util.get_flora_ids()
    arg_parser.add_argument(
        '--flora-id', '-e', action='append',
        choices=[str(k) for k in flora_ids],
        help="""Which flora ID to extract. Default 1.""")

    arg_parser.add_argument(
        '--html-file', '-H', type=argparse.FileType('w'),
        help="""Output the results to this HTML file.""")

    arg_parser.add_argument(
        '--sqlite3', '-S', help="""Output to this sqlite3 database.""")

    # arg_parser.add_argument(
    #     '--duckdb', '-D', help="""Output to this duckDB database.""")

    arg_parser.add_argument(
        '--csv-file', '-C', type=argparse.FileType('w'),
        help="""Output the results to this CSV file.""")

    arg_parser.add_argument(
        '--ner-file', '-N', type=argparse.FileType('a'),
        help="""Append formatted NER training data to this file.""")

    arg_parser.add_argument(
        '--iob-file', '-I', type=argparse.FileType('a'),
        help="""Append formatted training data in IOB format
            to this file.""")

    arg_parser.add_argument(
        '--biluo-file', '-B', type=argparse.FileType('a'),
        help="""Append formatted training data in BILUO format
            to this file.""")

    arg_parser.add_argument(
        '--list-families', '-l', action='store_true',
        help="""List families available to extract and exit.""")

    arg_parser.add_argument(
        '--clear-db', action='store_true',
        help="""Clear the duck_db before writing to it.""")

    args = arg_parser.parse_args()

    if args.family:
        args.family = [f.lower() for f in args.family]
    else:
        args.family = []

    if args.flora_id:
        args.flora_id = [int(i) for i in args.flora_id]
    else:
        args.flora_id = [1]

    if not (args.csv_file or args.html_file or args.ner_file or args.iob_file
            or args.biluo_file or args.sqlite3 or args.duckdb):
        setattr(args, 'csv_file', sys.stdout)

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
