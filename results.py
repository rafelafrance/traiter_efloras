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
                traits = [('agree', r) for r in results['correct']]
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


if __name__ == '__main__':
    main()
