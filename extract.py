#!/usr/bin/env python3

"""Use a custom ruler to parse efloras pages."""

import argparse
import sys
import textwrap

import efloras.pylib.family_util as futil
from efloras.readers.efloras_reader import efloras_reader
from efloras.writers.csv_writer import csv_writer
from efloras.writers.html_writer import html_writer

OUTPUT_FORMATS = {
    'csv': csv_writer,
    'html': html_writer}


def main(args):
    """Perform actions based on the arguments."""
    families = {k: v for k, v in futil.get_families().items() if v['count']}

    if args.list_families:
        futil.print_families(families)
        sys.exit()

    if not futil.check_family_flora_ids(args, families):
        sys.exit(1)

    rows = efloras_reader(args, families)
    OUTPUT_FORMATS[args.output_format](args, rows)


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
        choices=[str(k) for k in flora_ids.keys()],
        help="""Which flora ID to extract. Default 1.""")

    arg_parser.add_argument(
        '--output-file', '-o', type=argparse.FileType('w'), default=sys.stdout,
        help="""Output the results to this file. Defaults to stdout.""")

    arg_parser.add_argument(
        '--output-format', '-O', default='csv', choices=OUTPUT_FORMATS.keys(),
        help="""Output the result in this format. The default is "csv".""")

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

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
