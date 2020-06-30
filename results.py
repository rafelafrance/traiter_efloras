#!/usr/bin/env python3

"""Show results from the model."""

import json
from pathlib import Path


def main():
    """Do it."""
    results_path = Path('.') / 'models' / 'results.json'
    with open(results_path) as in_file:
        for line in in_file:
            sent, results = json.loads(line)
            if (results['missing']) or (results['excess']):
                print('=' * 120)
                print(sent)
                print('-' * 80)
                for result in sorted(results['agree']):
                    print(
                        f'Agree:   {result[2]:<15} '
                        f'[{sent[result[0]:result[1]]}]')
                print('-' * 80)
                for result in sorted(results['missing']):
                    print(
                        f'Missing: {result[2]:<15} '
                        f'[{sent[result[0]:result[1]]}]')
                print('-' * 80)
                for result in sorted(results['excess']):
                    print(
                        f'Excess:  {result[2]:<15} '
                        f'[{sent[result[0]:result[1]]}]')
                print()


if __name__ == '__main__':
    main()
