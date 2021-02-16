"""Write data to a database."""

import os
import sqlite3
from datetime import datetime

import duckdb
import pandas as pd

from efloras.pylib.const import PROCESSED_DATA, SITE

FIELD_SKIPS = """ source_id trait_id """.split()


def database(args, rows):
    """Write data to a database."""
    path = get_db_path(args)
    clear_db(args, path)

    cxn = connect(args, path)
    create_tables(cxn)

    source_df = get_sources(rows)
    cxn.register('source_df', source_df)

    taxon_df = get_taxa(rows)
    cxn.register('taxon_df', taxon_df)

    raw_traits = get_raw_traits(rows, cxn)
    from pprint import pp
    pp(raw_traits)

    trait_df, field_df = get_traits(raw_traits)
    cxn.register('trait_df', trait_df)
    cxn.register('field_df', field_df)

    delete_old_recs(cxn)
    inset_new_recs(cxn)

    drop_views(cxn)
    cxn.close()


def drop_views(cxn):
    """Remove data frame views."""
    cxn.execute('DROP VIEW source_df;')
    cxn.execute('DROP VIEW taxon_df;')
    cxn.execute('DROP VIEW trait_df;')
    cxn.execute('DROP VIEW field_df;')


def inset_new_recs(cxn):
    """Add the new data."""
    cxn.execute("""INSERT INTO sources SELECT * FROM source_df;""")
    cxn.execute("""INSERT INTO traits SELECT * FROM trait_df;""")
    cxn.execute("""INSERT INTO fields SELECT * FROM field_df;""")
    cxn.execute("""
        INSERT INTO taxa
        SELECT * FROM taxon_df
         WHERE taxon_df.taxon NOT IN (SELECT taxon FROM taxa);
    """)


def delete_old_recs(cxn):
    """Remove old records before inserting new ones."""
    cxn.execute("""
        DELETE FROM sources WHERE source_id IN (SELECT source_id FROM source_df);
    """)
    cxn.execute("""
        DELETE FROM traits WHERE source_id IN (SELECT source_id FROM source_df);
    """)
    cxn.execute("""
        DELETE FROM fields WHERE source_id IN (SELECT source_id FROM source_df);
    """)


def get_traits(raw_traits):
    """Build traits data frame."""
    trait_df = []
    field_df = []
    for trait in raw_traits:
        trait_df.append({
            'trait_id': trait['trait_id'],
            'source_id': trait['source_id'],
            'trait': trait['trait'],
            'taxon': trait['taxon'],
            'part': trait.get('part', ''),
            'sex': trait.get('sex', ''),
            'notes': '',
        })

        for field, value in trait.items():
            if field in ():
                continue
            if isinstance(value, list):
                for val in value:
                    append_value(field_df, trait, field, val)
            else:
                append_value(field_df, trait, field, value)

    trait_df = pd.DataFrame(trait_df)
    field_df = pd.DataFrame(field_df)

    return trait_df, field_df


def append_value(field_df, trait, field, value):
    """Append a value record to the data frame."""
    if field in FIELD_SKIPS:
        return

    field_df.append({
        'trait_id': trait['trait_id'],
        'source_id': trait['source_id'],
        'field': field,
        'string_value': value if isinstance(value, str) else None,
        'int_value': value if isinstance(value, int) else None,
        'float_value': value if isinstance(value, float) else None,
    })


def get_raw_traits(rows, cxn):
    """Create traits data frame."""
    traits = []
    next_id = get_max_trait_id(cxn)

    for row in rows:

        # Calculate entity IDs
        ents = []
        for ent in row['doc'].ents:
            next_id += 1
            ents.append([next_id, ent._.data, dict(ent._.links)])

        # Convert entity indices into trait IDs & append it to the list
        for ent in ents:
            ent[2] = {k: [ents[i][0] for i in v] for k, v in ent[2].items()}
            traits.append(
                ent[1] | ent[2] |
                {
                    'trait_id': ent[0],
                    'source_id': row['source_id'],
                    'taxon': row['taxon'],
                })

    return traits


def get_max_trait_id(cxn):
    """Get the max index for the table."""
    return cxn.execute('SELECT MAX(trait_id) FROM traits;').fetchone()[0] or 0


def get_taxa(rows):
    """Build taxa data frame."""
    df = []
    for row in rows:
        family = row['family'].capitalize()

        taxon = row['taxon'].capitalize()
        taxon_parts = taxon.split()

        if taxon == family:
            level = 'family'
            genus = ''
            species = ''

        elif len(taxon_parts) == 1:
            level = 'genus'
            genus = taxon_parts[0]
            species = ''

        elif len(taxon_parts) == 2:
            level = 'species'
            genus = taxon_parts[0]
            species = ' '.join(taxon_parts[:2])

        elif taxon.lower().find('subsp.') > -1:
            level = 'subspecies'
            genus = taxon_parts[0]
            species = ' '.join(taxon_parts[:2])

        elif taxon.lower().find('var.') > -1:
            level = 'variant'
            genus = taxon_parts[0]
            species = ' '.join(taxon_parts[:2])

        else:
            raise ValueError(f"Unknown level: {row['level']}")

        taxon = {
            'taxon': row['taxon'],
            'level': level,
            'family': family,
            'genus': genus,
            'species': species,
            'notes': '',
        }
        df.append(taxon)

    df = pd.DataFrame(df)
    return df


def get_sources(rows):
    """Build sources data frame."""
    df = []
    for row in rows:
        # Put the file modified date into ISO 8601 format.
        downloaded = os.stat(row['path']).st_mtime
        downloaded = datetime.fromtimestamp(downloaded)
        downloaded = downloaded.isoformat(sep=' ', timespec='seconds')

        source_id = row['taxon_id'] * 1000 + row['flora_id']

        source = {
            'source_id': source_id,
            'source': SITE,
            'url': row['link'],
            'downloaded': downloaded,
            'notes': f"{row['family']}, {row['flora_name']}, {row['taxon']}"
        }
        df.append(source)
        row['source_id'] = source_id

    df = pd.DataFrame(df)
    return df


def get_tables(cxn):
    """Check if the database is empty."""
    tables = cxn.execute('PRAGMA show_tables;').fetchall()
    return tables


def connect(args, path):
    """Connect to the database."""
    path = str(path)
    return duckdb.connect(path) if args.duckdb else sqlite3.connect(path)


def clear_db(args, path):
    """Connect to the database."""
    if args.clear_db:
        wal = PROCESSED_DATA / (path.name + '.wal')
        wal.unlink(missing_ok=True)
        path.unlink(missing_ok=True)


def get_db_path(args):
    """Connect to the database."""
    name = 'efloras.duckdb.db' if args.duckdb else 'efloras.sqlite3.db'
    return PROCESSED_DATA / name


def create_tables(cxn):
    """Create tables and indices."""
    cxn.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            source_id  UBIGINT PRIMARY KEY,
            source     VARCHAR,
            url        VARCHAR,
            downloaded DATE,
            notes      VARCHAR
        );
    """)

    cxn.execute("""
        CREATE TABLE IF NOT EXISTS taxa (
            taxon   VARCHAR PRIMARY KEY,
            level   VARCHAR,
            family  VARCHAR,
            genus   VARCHAR,
            species VARCHAR,
            notes   VARCHAR
        );
    """)

    cxn.execute("""
        CREATE TABLE IF NOT EXISTS traits (
            trait_id  UBIGINT PRIMARY KEY,
            source_id UBIGINT,
            trait     VARCHAR,
            taxon     VARCHAR,
            part      VARCHAR,
            sex       VARCHAR,
            notes     VARCHAR
        );
    """)

    cxn.execute("""
        CREATE TABLE IF NOT EXISTS fields (
            trait_id     UBIGINT,
            source_id    UBIGINT,
            field        VARCHAR,
            string_value VARCHAR,
            int_value    BIGINT,
            float_value  DOUBLE
        );
    """)
