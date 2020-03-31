#!/usr/bin/env python3

"""Parse extracted efloras web pages."""

import sys
import argparse
import textwrap
import efloras.pylib.family_util as futil
import efloras.pylib.trait_groups as tg
from efloras.writers.html_writer import html_writer
from efloras.writers.csv_writer import csv_writer
from efloras.readers.efloras_reader import efloras_reader


INPUT_FORMATS = {
    'efloras': efloras_reader}

OUTPUT_FORMATS = {
    'csv': csv_writer,
    'html': html_writer}


def main(args):
    """Perform actions based on the arguments."""
    families = {k: v for k, v in futil.get_families().items() if v['count']}

    if args.list_families:
        futil.print_families(families)
        sys.exit()

    if args.list_traits:
        for trait in tg.TRAIT_NAMES:
            print(trait)
        sys.exit()

    if not futil.check_family_flora_ids(args, families):
        sys.exit(1)

    if not (traits := tg.expand_traits(args)):
        print(f'No traits match: {" or ".join(args.trait)}.')
        sys.exit(1)
    setattr(args, 'trait', traits)

    parse_traits(args, families)


def parse_traits(args, families):
    """Perform actions based on the arguments."""
    df = INPUT_FORMATS[args.input_format](args, families)
    OUTPUT_FORMATS[args.output_format](args, df)


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from the eFloras website."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--family', '-f', action='append',
        help="""Which family to extract.""")

    arg_parser.add_argument(
        '--trait', '-t', action='append',
        help="""The traits to extract.""")

    flora_ids = futil.get_flora_ids()
    arg_parser.add_argument(
        '--flora-id', '--id', '-F', action='append',
        choices=[str(k) for k in flora_ids.keys()],
        help="""Which flora ID to download. Default 1.""")

    arg_parser.add_argument(
        '--input-format', '-I', default='efloras',
        choices=INPUT_FORMATS.keys(),
        help="""The data input format. The default is "efloras".""")

    arg_parser.add_argument(
        '--output-file', '-o', type=argparse.FileType('w'), default=sys.stdout,
        help="""Output the results to this file. Defaults to stdout.""")

    arg_parser.add_argument(
        '--output-format', '-O', default='csv', choices=OUTPUT_FORMATS.keys(),
        help="""Output the result in this format. The default is "csv".""")

    arg_parser.add_argument(
        '--list-families', '-l', action='store_true',
        help="""List families available to extract and exit.""")

    arg_parser.add_argument(
        '--list-traits', '-T', action='store_true',
        help="""List traits available to extract and exit.""")

    args = arg_parser.parse_args()

    if args.family:
        args.family = [f.lower() for f in args.family]

    if args.flora_id:
        args.flora_id = [int(i) for i in args.flora_id]

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)