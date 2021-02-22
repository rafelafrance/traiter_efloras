"""Write data to a duck_db."""

from pathlib import Path

import duckdb

from efloras.pylib.const import PROCESSED_DATA
from efloras.writers.sqlite3_db import get_raw_traits, get_sources, get_taxa, get_traits

FIELD_SKIPS = """ source_id trait_id """.split()


def duck_db(args, rows):
    """Write data to a duck_db."""
    path = Path(args.duckdb)
    clear_db(args, path)

    cxn = duckdb.connect(str(path))

    create_tables(cxn)

    source_df = get_sources(rows)
    cxn.register('source_df', source_df)

    taxon_df = get_taxa(rows)
    cxn.register('taxon_df', taxon_df)

    raw_traits = get_raw_traits(rows, cxn)

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
        DELETE FROM sources WHERE source_id IN (SELECT source_id FROM source_df);""")
    cxn.execute("""
        DELETE FROM traits WHERE source_id IN (SELECT source_id FROM source_df);""")
    cxn.execute("""
        DELETE FROM fields WHERE source_id IN (SELECT source_id FROM source_df);""")


def clear_db(args, path):
    """Clear to the DB."""
    if args.clear_db:
        wal = PROCESSED_DATA / (path.name + '.wal')
        wal.unlink(missing_ok=True)
        path.unlink(missing_ok=True)


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
