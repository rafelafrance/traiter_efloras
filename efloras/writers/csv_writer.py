"""Write the output to a CSV file."""

import efloras.pylib.util as util


def csv_writer(args, df):  # pylint: disable=unused-argument
    """Output the data frame."""
    data = df.fillna('').to_dict('records')
    print(df.columns)
    print(args)
    data = merge_duplicates(args, data)
    # df.to_csv(args.output_file, index=False)
    # rows = [x.to_dict() for i, x in df.iterrows()]


def merge_duplicates(args, data):
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
        ]
    """
    LOCATION = ['start', 'end', 'trait_group']
    KEYS = ['value', 'part']
    SKIP = LOCATION + KEYS

    for row in data:
        new_row = {}

        for header, cell in row.items():

            # If it isn't a trait then just copy it over to the new row
            if header not in args.trait:
                new_row[header] = cell
                continue

            dupes = {}

            # Loop thru list of trait parses in the cell & merge duplicates
            for trait in cell:

                # Get location values. These get merged into a single column
                location = {k: v for k, v in trait.items() if k in LOCATION}

                # Get everthing else. These are kept as separate columns
                fields = {k: v for k, v in trait.items() if k not in LOCATION}

                # We consider this a unique value
                key = tuple((
                    util.as_tuple(trait['value']),
                    trait.get('part', '')))

                if dupe := dupes.get(key):
                    dupe['location'].append(location)
                    # for key, value in fields.items():
                else:
                    dupes[key]['location'] = [location]
                    dupes[key] = fields

            values = []

    return data

# import regex
# import pandas as pd
# # from pylib.all_traits import TRAITS
# from pylib.writers.base_writer import BaseWriter
#
#
# class CsvWriter(BaseWriter):
#     """Write the lib output to a file."""
#
#     def __init__(self, args):
#         """Build the writer."""
#         super().__init__(args)
#         self.columns = args.extra_field
#         self.columns += args.search_field
#       self.columns += sorted({f for fds in args.as_is.values() for f in fds})
#
#     def start(self):
#         """Start the report."""
#         self.rows = []
#
#     def record(self, raw_record, parsed_record):
#         """Output a row to the file."""
#         self.progress()
#
#         row = {c: raw_record.get(c, '') for c in self.columns}
#
#         self.rows.append(row)
#
#     def end(self):
#         """End the report."""
#         df = pd.DataFrame(self.rows)
#         df.rename(columns=lambda x: regex.sub(r'^.+?:\s*', '', x),
#               inplace=True)
#         df.to_csv(self.args.output_file, index=False)
