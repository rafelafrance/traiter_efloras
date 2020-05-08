"""Write the output to a CSV file."""

from collections import defaultdict

import pandas as pd

import efloras.pylib.family_util as futil
import efloras.pylib.util as util


def csv_writer(args, df):
    """Output the data frame."""
    # Split the family name/flora ID into separate columns
    df = merge_duplicates(args, df)
    df.to_csv(args.output_file, index=False)


def merge_duplicates(args, df):
    """Merge duplicate extracts.

    If the same trait value is extracted multiple times then we merge those
    duplicated values but still report the multiple places where the trait was
    extracted. We are giving each extracted value a separate column. Like so:
        "color": [
            {"value": "red", "start": 10, "end": 13},
            {"value": "red", "start": 20, "end": 23},
            {"value": "blue", "start": 30, "end": 34},
        ]
    becomes:
        "color_1":
            {"value": "red", "location": [
                {"start": 10, "end": 13},
                {"start": 20, "end": 23}]},
         "color_2: {"value": "blue", "location": {"start": 30, "end": 34}}
    """
    data = df.fillna('').to_dict('records')

    location_fields = ('start', 'end', 'trait_group')
    key_fields = ('value', 'part')

    new_data = []

    for row in data:
        new_row = {}

        for header, cell in row.items():

            # If it isn't a trait then just copy it over to the new row
            if header not in args.trait:
                new_row[header] = cell
                continue

            dupes = defaultdict(lambda: defaultdict(set))

            # Loop thru list of trait parses in the cell & merge duplicates
            for trait in cell:

                # The unique value
                unique = tuple(util.as_tuple(sorted(util.as_list(v)))
                               for k, v in trait.items() if k in key_fields)

                # Merge locations into a single field
                location = tuple((k, v) for k, v in trait.items()
                                 if k in location_fields)
                dupes[unique]['location'].add(location)

                # Add other values
                for key, value in trait.items():
                    if key not in location_fields:
                        dupes[unique][key].add(util.as_member(value))

            # Pivot the separate extracts
            for i, dupe in enumerate(dupes.values(), 1):
                # Pivot fields for each extract
                for field, value in dupe.items():
                    if field == 'location':
                        value = [{k: v for k, v in loc} for loc in value]
                    else:
                        value = util.flatten(value)
                    new_row[f'{header}_{i}_{field}'] = util.squash(value)

        new_data.append(new_row)

    # Build a dataframe and move some columns
    df = pd.DataFrame(new_data)
    df = df.sort_index(axis=1)

    for name in """ taxon_id taxon flora_id flora_name family """.split():
        column = df.pop(name)
        df.insert(0, name, column)

    for name in """ text link """.split():
        column = df.pop(name)
        df.insert(len(df.columns), name, column)

    return df
