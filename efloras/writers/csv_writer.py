"""Write the output to a CSV file."""

from collections import defaultdict

import pandas as pd

from ..pylib.util import convert


def csv_writer(args, rows):
    """Output the data frame."""
    rows = sorted(rows, key=lambda r: (r['flora_id'], r['family'], r['taxon']))

    for row in rows:
        row['raw_traits'] = dict(row['traits'])
        del row['traits']
        build_columns(row)

    df = pd.DataFrame(rows)
    df.to_csv(args.csv_file, index=False)


def build_columns(row):
    """Expand values into separate columns."""
    extras = set(""" sex location as """.split())
    skips = extras | {'start', 'end'}

    for label, traits in row['raw_traits'].items():
        if label in ('part', 'subpart'):
            continue
        columns = defaultdict(list)
        for trait in traits:
            header = sorted(v for k, v in trait.items() if k in extras)
            header = '.'.join([label] + header)
            value = {k: v for k, v in trait.items() if k not in skips}
            columns[header].append(value)

        for header, value_list in columns.items():
            is_vocab = [len(v) == 1 and v.get('value') for v in value_list]
            if all(is_vocab):
                value = {v['value'] for v in value_list}
                row[header] = ', '.join(sorted(value))
            elif header.endswith('_size'):
                extract_sizes(row, header, value_list)
            else:
                extract_traits(row, header, value_list)

    return row


def extract_traits(row, header, value_list):
    """Extract non-size & non-value list traits."""
    for i, extract in enumerate(value_list, 1):
        for field, value in extract.items():
            key = f'{header}.{i}.{field}'
            row[key] = value


def extract_sizes(row, header, value_list):
    """Normalize size traits."""
    for i, extract in enumerate(value_list, 1):

        length_units = extract.get(
            'length_units', extract.get('width_units'))
        width_units = extract.get(
            'width_units', extract.get('length_units'))

        for field, value in extract.items():
            key = f'{header}.{i}.{field}'
            if field.endswith('_units'):
                row[key] = value
            elif field.startswith('length_'):
                row[key] = convert(value, length_units)
            elif field.startswith('width_'):
                row[key] = convert(value, width_units)
