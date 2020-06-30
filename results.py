#!/usr/bin/env python3

"""Show results from the model."""

import argparse
import json
import textwrap


def main(args):
    """Do it."""
    if args.confusion_matrix:
        confusion_matrix(args)

    if args.error_detail:
        error_detail(args)


def confusion_matrix(args):
    """Output a confusion matrix."""


def error_detail(args):
    """Output the error detail report."""
    for line in args.results_file:
        sent, results = json.loads(line)
        if (results['missing']) or (results['excess']):
            traits = [('agree', r) for r in results['agree']]
            traits += [('MISSING', r) for r in results['missing']]
            traits += [('EXCESS', r) for r in results['excess']]
            traits = sorted(traits, key=lambda t: (t[1][0], t[1][1]))
            print('=' * 120)
            print(sent)
            print('-' * 80)
            for result in traits:
                flag = ' ' if result[0] == 'agree' else '*'
                print(
                    f'{result[0]:<7} {flag} {result[1][2]:<15} '
                    f'{sent[result[1][0]:result[1][1]]}')
            print()


def parse_args():
    """Process command-line arguments."""
    description = """Create models from data from the eFloras website."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--results-file', '-r', type=argparse.FileType(), required=True,
        help="""Read data from this file.""")

    arg_parser.add_argument(
        '--confusion-matrix', '-s', action='store_true',
        help="""Print a confusion matrix of the results.""")

    arg_parser.add_argument(
        '--error-detail', '-e', action='store_true',
        help="""Print a detailed error report.""")

    args = arg_parser.parse_args()
    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
