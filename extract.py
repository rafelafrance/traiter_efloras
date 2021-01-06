#!/usr/bin/env python3

"""Parse src treatments."""

import argparse
import sys
import textwrap
from copy import deepcopy
from itertools import product

import src.pylib.util
from src.matchers.pipeline import Pipeline
from src.readers.efloras import efloras_reader
from src.writers.csv_ import csv_writer
from src.writers.data import biluo_writer, iob_writer, ner_writer
from src.writers.html_ import html_writer


def get_efloras_families(args):
    """Handle eFloras extractions"""
    families = {k: v for k, v in src.pylib.util.get_families().items() if v['count']}

    if not check_family_flora_ids(args, families):
        sys.exit(1)

    if args.list_families:
        print_families(families)
        sys.exit()

    return families


def main(args):
    """Perform actions based on the arguments."""
    pipeline = Pipeline()
    families = get_efloras_families(args)

    rows = efloras_reader(args, families)

    for row in rows:
        row['doc'] = pipeline.nlp(row['text'])
        row['traits'] = pipeline.trait_list(row['doc'])

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


def get_family_flora_ids(args, families):
    """Get family and flora ID combinations."""
    return [c for c in product(args.family, args.flora_id)
            if c in families]


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

    flora_ids = src.pylib.util.get_flora_ids()
    arg_parser.add_argument(
        '--flora-id', '-e', action='append',
        choices=[str(k) for k in flora_ids],
        help="""Which flora ID to extract. Default 1.""")

    arg_parser.add_argument(
        '--html-file', '-H', type=argparse.FileType('w'),
        help="""Output the results to this HTML file.""")

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
            or args.biluo_file):
        setattr(args, 'csv_file', sys.stdout)

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
