"""Write data to a database."""

import os
import sqlite3
from datetime import datetime
from pprint import pp

import duckdb
import pandas as pd

from efloras.pylib.const import PROCESSED_DATA, SITE


def database(args, rows):
    """Write data to a database."""
    path = get_db_path(args)
    clear_db(args, path)

    cxn = connect(args, path)
    create_tables(cxn)

    print(get_tables(cxn))

    source_df = get_sources(rows)
    pp(source_df.shape)

    taxon_df = get_taxa(rows)
    pp(taxon_df.shape)

    raw_traits = get_raw_traits(rows, cxn)
    pp(raw_traits)

    trait_df, value_df = get_traits(raw_traits)

    cxn.close()


def get_traits(raw_traits):
    """Build traits data frame."""
    trait_df = []
    value_df = []
    for trait in raw_traits:
        trait_df.append({
            'trait_id': trait['trait_id'],
            'source_id': trait['source_id'],
            'trait': trait['trait'],
            'taxon': trait['taxon'],
            'sex': trait.get('sex', ''),
            'notes': '',
        })

        for field, value in trait.items():
            if field in ():
                continue
            if isinstance(value, list):
                for val in value:
                    append_value(value_df, trait, field, val)
            else:
                append_value(value_df, trait, field, value)

    return trait_df, value_df


def append_value(value_df, trait, field, value):
    """Append a value record to the data frame."""
    value_df.append({
        'trait_id': trait['trait_id'],
        'source_id': trait['source_id'],
        'field': field,
        'string': value if isinstance(value, str) else None,
        'number': value if not isinstance(value, str) else None,
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
                    'taxon': row['taxon'],
                    'source_id': row['source_id'],
                })

    return traits


def get_max_trait_id(cxn):
    """Get the max index for the table."""
    return cxn.execute('SELECT MAX(trait_id) FROM traits;').fetchone()[0] or 0


def get_taxa(rows):
    """Build taxa data frame."""
    df = []
    for row in rows:
        taxon = row['taxon']
        level = taxon.split()
        if len(level) == 1 and taxon.lower() == row['family'].lower():
            level = 'family'
        elif len(level) == 1:
            level = 'genus'
        elif len(level) == 2:
            level = 'species'
        elif taxon.lower().find('subsp.') > -1:
            level = 'subspecies'
        elif taxon.lower().find('var.') > -1:
            level = 'variant'
        else:
            raise ValueError(f"Unknown level: {row['level']}")

        taxon = {
            'taxon': row['taxon'],
            'level': level,
            'notes': '',
        }
        df.append(taxon)

    df = pd.DataFrame(df)
    df = df.set_index('taxon')
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
    df = df.set_index('source_id')
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
            taxon  VARCHAR PRIMARY KEY,
            level  VARCHAR,
            notes  VARCHAR
        );
    """)

    cxn.execute("""
        CREATE TABLE IF NOT EXISTS traits (
            trait_id  UBIGINT PRIMARY KEY,
            source_id UBIGINT,
            trait     VARCHAR,
            taxon     VARCHAR,
            part      VARCHAR,
            notes     VARCHAR
        );
    """)

    cxn.execute("""
        CREATE TABLE IF NOT EXISTS values (
            trait_id  UBIGINT,
            source_id UBIGINT,
            field     VARCHAR,
            string    VARCHAR,
            number    REAL
        );
    """)
