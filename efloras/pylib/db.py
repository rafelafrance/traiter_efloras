"""Common functions for dealing with the database."""

import sqlite3
from pathlib import Path

ITIS_DB = Path('.') / 'data' / 'itis' / 'ITIS.sqlite'
PLANTAE = 3


def connect(path: str = ITIS_DB) -> sqlite3.Connection:
    """Connect to an SQLite database."""
    cxn = sqlite3.connect(path)

    cxn.execute('PRAGMA page_size = {}'.format(2 ** 16))
    cxn.execute('PRAGMA busy_timeout = 10000')
    cxn.execute('PRAGMA journal_mode = WAL')
    cxn.row_factory = sqlite3.Row
    return cxn


def select_taxa(cxn: sqlite3.Connection) -> sqlite3.Cursor:
    """Get taxonomic names."""
    return cxn.execute(
        """SELECT complete_name
             FROM taxonomic_units
            WHERE kingdom_id = ?;""",
        (PLANTAE, ))


def select_taxon_names(cxn: sqlite3.Connection) -> sqlite3.Cursor:
    """Get taxonomic names."""
    return cxn.execute(
        """SELECT rank_name
             FROM taxon_unit_types
            WHERE kingdom_id = ?;""",
        (PLANTAE, ))
