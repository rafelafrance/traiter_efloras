from collections import defaultdict

from plants.patterns import term_patterns as terms
from plants.writers import csv_writer as base_writer


class CsvWriter(base_writer.CsvWriter):
    @staticmethod
    def sort_columns(df):
        first = """
            family flora_id flora_name taxon taxon_id link path text raw_traits
            """.split()
        rest = sorted(c for c in df.columns if c not in first)
        columns = first + rest

        df = df[columns]

        return df

    def format_row(self, row):
        csv_row = {
            "family": row.family,
            "flora_id": row.flora_id,
            "flora_name": row.flora_name,
            "taxon": row.taxon,
            "taxon_id": row.taxon_id,
            "link": row.link,
            "path": row.path,
            "text": row.text,
            "raw_traits": row.traits,
        }

        by_header = defaultdict(list)
        for trait in row.traits:
            if trait["trait"] in terms.PARTS_SET:
                continue

            key_set = set(trait.keys())

            if not (terms.PARTS_SET & key_set):
                continue

            base_header = self.base_column_header(trait)

            self.group_values_by_header(by_header, trait, base_header)

        return csv_row

    @staticmethod
    def base_column_header(trait):
        if "subpart" in trait:
            label = f'{trait["part"]}_{trait["subpart"]}_{trait["trait"]}'
        elif "subpart_suffix" in trait:
            subpart = trait["subpart_suffix"].removeprefix("-")
            label = f'{trait["part"]}_{subpart}_{trait["trait"]}'
        else:
            label = f'{trait["part"]}_{trait["trait"]}'
        return label

    @staticmethod
    def group_values_by_header(by_header, trait, base_header):
        extras = sorted(v for k, v in trait.items() if k in base_writer.EXTRAS)
        unnumbered_header = "_".join([base_header] + extras)
        trait = {k: v for k, v in trait.items() if k not in base_writer.SKIP}
        by_header[unnumbered_header].append(trait)

    @staticmethod
    def number_columns(by_header, csv_row):
        for unnumbered_header, trait_list in by_header.items():
            for i, trait in enumerate(trait_list):
                for key, value in trait.items():
                    header = f"{unnumbered_header}.{i}.{key}"
                    csv_row[header] = value
