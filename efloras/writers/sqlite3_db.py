"""Write data to a duck_db."""

import os
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

from efloras.pylib.const import SITE


def sqlite3_db(args, rows):
    """Write data to a duck_db."""
    path = Path(args.sqlite3)

    if args.clear_db:
        path.unlink(missing_ok=True)

    cxn = sqlite3.connect(str(path))

    create_tables(cxn)

    source_df = get_sources(rows)
    taxon_df = get_taxa(rows, cxn)
    raw_traits = get_raw_traits(rows, cxn)
    trait_df, field_df = get_traits(raw_traits)

    delete_old_recs(cxn)

    source_df.to_sql('sources', cxn, if_exists='append', index=False)
    taxon_df.to_sql('taxa', cxn, if_exists='append', index=False)
    trait_df.to_sql('traits', cxn, if_exists='append', index=False)
    field_df.to_sql('fields', cxn, if_exists='append', index=False)

    cxn.close()


def delete_old_recs(cxn):
    """Remove old records before inserting new ones."""
    cxn.executescript("""
        DELETE FROM sources WHERE source_id IN (SELECT source_id FROM source_ids);
        DELETE FROM traits WHERE source_id IN (SELECT source_id FROM source_ids);
        DELETE FROM fields WHERE source_id IN (SELECT source_id FROM source_ids);
    """)


def get_traits(raw_traits):
    """Build traits data frame."""
    trait_df = []
    field_df = []

    for trait in raw_traits:

        if trait['trait'] in ('dimension', 'units'):
            continue

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
    if field in ('source_id', 'trait_id'):
        return

    field_df.append({
        'trait_id': trait['trait_id'],
        'source_id': trait['source_id'],
        'field': field,
        'value': value,
    })


def get_raw_traits(rows, cxn):
    """Create traits data frame."""
    traits = []
    next_id = get_max_trait_id(cxn)

    for row in rows:
        all_ents = {}

        # Create an ID and key entities by their span start & end characters
        for ent in row['doc'].ents:
            next_id += 1
            all_ents[(ent.start_char, ent.end_char)] = {
                'id': next_id,
                'data': ent._.data,
                'links': dict(ent._.links),  # Links are by token indices
            }

        # Convert entity indices into trait IDs & append it to the list
        for ent in all_ents.values():
            link_ids = {k: all_ents[i]['id']
                        for k, v in ent['links'].items() for i in v}
            traits.append(
                ent['data'] | link_ids | {
                    'trait_id': ent['id'],
                    'source_id': row['source_id'],
                    'taxon': row['taxon'],
                })

    return traits


def get_max_trait_id(cxn):
    """Get taxa already in the database."""
    return cxn.execute('SELECT MAX(trait_id) FROM traits;').fetchone()[0] or 0


def get_taxa(rows, cxn):
    """Build taxa data frame."""
    existing = {r[0] for r in cxn.execute('SELECT taxon FROM taxa;').fetchall()}

    df = []
    for row in rows:
        taxon = row['taxon'].capitalize()

        if taxon in existing:
            continue

        existing.add(taxon)

        family = row['family'].capitalize()

        level, genus, species = get_taxon_level(family, taxon)

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


def get_taxon_level(family, taxon):
    """Calculate the taxon level and any """
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

    elif taxon.lower().find('sect.') > -1:
        level = 'section'
        genus = taxon_parts[0]
        species = ''

    else:
        raise ValueError(f"Cannot find taxon level in: {taxon}")

    return level, genus, species


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
            'text_': row['text'],
            'downloaded': downloaded,
            'notes': f"{row['family']}, {row['flora_name']}, {row['taxon']}"
        }
        df.append(source)
        row['source_id'] = source_id

    df = pd.DataFrame(df)
    return df


def create_tables(cxn):
    """Create tables and indices."""
    cxn.executescript("""
        CREATE TABLE IF NOT EXISTS sources (
            source_id  INTEGER PRIMARY KEY,
            source     TEXT,
            url        TEXT,
            text_      TEXT,
            downloaded DATE,
            notes      TEXT
        );
        CREATE INDEX IF NOT EXISTS sources_source ON sources (source);
    """)

    cxn.executescript("""
        CREATE TABLE IF NOT EXISTS taxa (
            taxon   TEXT PRIMARY KEY,
            level   TEXT,
            family  TEXT,
            genus   TEXT,
            species TEXT,
            notes   TEXT
        );
        CREATE INDEX IF NOT EXISTS taxa_level ON taxa (level);
        CREATE INDEX IF NOT EXISTS taxa_family ON taxa (family);
        CREATE INDEX IF NOT EXISTS taxa_genus ON taxa (genus);
        CREATE INDEX IF NOT EXISTS taxa_species ON taxa (species);
    """)

    cxn.executescript("""
        CREATE TABLE IF NOT EXISTS traits (
            trait_id  INTEGER PRIMARY KEY,
            source_id INTEGER,
            trait     TEXT,
            taxon     TEXT,
            part      TEXT,
            sex       TEXT,
            notes     TEXT
        );
        CREATE INDEX IF NOT EXISTS traits_source_id ON traits (source_id);
        CREATE INDEX IF NOT EXISTS traits_trait ON traits (trait);
        CREATE INDEX IF NOT EXISTS traits_taxon ON traits (taxon);
        CREATE INDEX IF NOT EXISTS traits_part ON traits (part);
        CREATE INDEX IF NOT EXISTS traits_sex ON traits (sex);
    """)

    cxn.executescript("""
        CREATE TABLE IF NOT EXISTS fields (
            trait_id  INTEGER,
            source_id INTEGER,
            field     TEXT,
            value
        );
        CREATE INDEX IF NOT EXISTS fields_source_id ON fields (source_id);
        CREATE INDEX IF NOT EXISTS fields_field ON fields (field);
    """)

    cxn.executescript("""
        CREATE TEMP TABLE source_ids (
            source_id INTEGER
        );
    """)
