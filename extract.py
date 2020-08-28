#!/usr/bin/env python3

"""Parse src treatments."""

import argparse
import sys
import textwrap
from copy import deepcopy

import src.pylib.family as futil
from src.pylib.pipeline import PIPELINE
from src.readers.efloras_reader import efloras_reader
from src.writers.csv_writer import csv_writer
from src.writers.data_writer import ner_writer
from src.writers.html_writer import html_writer


def main(args):
    """Perform actions based on the arguments."""
    families = {k: v for k, v in futil.get_families().items() if v['count']}

    if args.list_families:
        futil.print_families(families)
        sys.exit()

    if not futil.check_family_flora_ids(args, families):
        sys.exit(1)

    rows = efloras_reader(args, families)

    # attach = not bool(args.ner_file)

    for row in rows:
        row['traits'] = PIPELINE.trait_list(row['text'])

    if args.csv_file:
        copied = deepcopy(rows)
        csv_writer(args, copied)

    if args.html_file:
        copied = deepcopy(rows)
        html_writer(args, copied)

    if args.ner_file:
        copied = deepcopy(rows)
        ner_writer(args, copied)


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from the eFloras website."""
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

    flora_ids = futil.get_flora_ids()
    arg_parser.add_argument(
        '--flora-id', '--id', '-F', action='append',
        choices=[str(k) for k in flora_ids],
        help="""Which flora ID to extract. Default 1.""")

    arg_parser.add_argument(
        '--html-file', '-H', type=argparse.FileType('w'),
        help="""Output the results to this HTML file.""")

    arg_parser.add_argument(
        '--csv-file', '-C', type=argparse.FileType('w'),
        help="""Output the results to this CSV file.""")

    arg_parser.add_argument(
        '--nel-file', '-N', type=argparse.FileType('a'),
        help="""Append formatted NEL data to this file.""")

    arg_parser.add_argument(
        '--ner-file', '-n', type=argparse.FileType('a'),
        help="""Append formatted NER data to this file.""")

    arg_parser.add_argument(
        '--list-families', '-l', action='store_true',
        help="""List families available to extract and exit.""")

    args = arg_parser.parse_args()

    if args.family:
        args.family = [f.lower() for f in args.family]
    else:
        args.family = []

    if args.flora_id:
        args.flora_id = [int(i) for i in args.flora_id]
    else:
        args.flora_id = [1]

    if not (args.csv_file or args.html_file or args.ner_file or args.nel_file):
        setattr(args, 'csv_file', sys.stdout)

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
