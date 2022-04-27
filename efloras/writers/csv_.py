"""Write the output to a CSV file."""
from collections import defaultdict

import pandas as pd

from efloras.pylib.util import convert


def csv_writer(args, rows):
    """Output the data."""
    rows = sorted(rows, key=lambda r: (r["flora_id"], r["family"], r["taxon"]))

    for row in rows:
        row["raw_traits"] = [e._.data for e in row["doc"].ents]
        del row["doc"]
        build_columns(row)

    df = pd.DataFrame(rows)
    df["raw_traits"] = None
    df.to_csv(args.csv_file, index=False)


def build_columns(row):
    """Expand values into separate columns."""
    extras = set(""" sex location group """.split())
    skips = extras | {"start", "end"}

    columns = defaultdict(list)
    for trait in row["raw_traits"]:
        if trait["trait"] in ("part", "subpart"):
            continue
        if "part" not in trait:
            continue

        if "subpart" in trait:
            label = f'{trait["part"]}_{trait["subpart"]}_{trait["trait"]}'
        else:
            label = f'{trait["part"]}_{trait["trait"]}'
        trait = {
            k: v for k, v in trait.items() if k not in ("part", "subpart", "trait")
        }
        header = sorted(v for k, v in trait.items() if k in extras)
        header = ".".join([label] + header)
        value = {k: v for k, v in trait.items() if k not in skips}
        columns[header].append(value)

    for header, value_list in columns.items():
        keys = set()
        all_strings = True
        for data in value_list:
            for key, value in data.items():
                keys.add(key)
                all_strings &= isinstance(value, str)

        if len(keys) == 1 and all_strings:
            value = {v[k] for v in value_list for k in v.keys()}
            row[header] = ", ".join(sorted(value))
        elif header.endswith("_size"):
            extract_sizes(row, header, value_list)
        else:
            extract_traits(row, header, value_list)

    return row


def extract_traits(row, header, value_list):
    """Extract non-size & non-value list traits."""
    for i, extract in enumerate(value_list, 1):
        for field, value in extract.items():
            key = f"{header}.{i}.{field}"
            row[key] = value


def extract_sizes(row, header, value_list):
    """Normalize size traits."""
    for i, extract in enumerate(value_list, 1):

        length_units = extract.get("length_units", extract.get("width_units"))
        width_units = extract.get("width_units", extract.get("length_units"))

        for field, value in extract.items():
            key = f"{header}.{i}.{field}"
            parts = field.split("_")
            if parts[0] in ("trait", "part", "subpart"):
                continue
            if len(parts) > 1 and parts[1] == "units":
                row[key] = value
            elif parts[0] == "length":
                row[key] = convert(value, length_units)
            elif parts[0] == "width":
                row[key] = convert(value, width_units)
            elif parts[0].endswith("units"):
                units = f"{parts[0]}_units"
                row[key] = convert(value, extract.get(units))
