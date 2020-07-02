#!/usr/bin/env python3

"""Show results from the model."""

import argparse
import json
import sys
import textwrap

import pandas as pd


def main(args):
    """Do it."""
    if args.confusion_matrix or args.confusion_csv:
        matrix(args)

    if args.error_detail:
        error_detail(args)


def matrix(args):
    """Output a confusion matrix."""
    expected = []
    actually = []
    for line in args.results_file:
        sent, results = json.loads(line)
        for result_dict in results:
            result = result_dict['result']
            expect = result_dict.get('expect')
            actual = result_dict.get('actual')
            if result == 'ok':
                expected.append(expect[2])
                actually.append(expect[2])
            elif actual and expect:
                expected.append(expect[2])
                actually.append(actual[2])
            elif expect:
                expected.append(expect[2])
                actually.append('~missing~')
            elif actual:
                expected.append('~missing~')
                actually.append(actual[2])
            else:
                sys.exit(result_dict)

    expected = pd.Series(expected)
    actually = pd.Series(actually)

    df = pd.crosstab(expected, actually, rownames=['Expected'],
                     colnames=['Predicted'], margins=True)

    if args.confusion_matrix:
        print(df.to_string())

    if args.confusion_csv:
        df.to_csv(args.confusion_csv)


def error_detail(args):
    """Output the error detail report."""
    for line in args.results_file:
        sent, results = json.loads(line)
        has_errors = any(r['result'] != 'ok' for r in results)
        if has_errors:
            print('=' * 100)
            print(sent)
            print('-' * 80)
            for result_dict in results:
                result = result_dict['result']
                expect = result_dict.get('expect')
                actual = result_dict.get('actual')
                if actual and expect:
                    print(
                        f'{result.upper():<6} '
                        f'expected ({expect[2]}) {sent[expect[0]:expect[1]]} '
                        f'got ({actual[2]}) {sent[actual[0]:actual[1]]}')
                elif expect:
                    print(f'{result:<6} expected and got '
                          f'({expect[2]}) {sent[expect[0]:expect[1]]}')
                else:
                    print(f'{result.upper():<6} '
                          f'got ({actual[2]}) {sent[actual[0]:actual[1]]}')
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
        '--confusion-matrix', '-c', action='store_true',
        help="""Print a confusion matrix of the results.""")

    arg_parser.add_argument(
        '--confusion-csv', '-C',
        help="""Output a confusion matrix of the results to this CSV file.""")

    arg_parser.add_argument(
        '--error-detail', '-e', action='store_true',
        help="""Print a detailed error report.""")

    args = arg_parser.parse_args()
    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
