"""Common functions for dealing with the database."""

import sqlite3
import subprocess
from datetime import datetime
from os import fspath, remove
from pathlib import Path

from .util import DATA_DIR, log

DB_FILE = DATA_DIR / 'efloras.sqlite.db'
SCRIPT_PATH = Path('sql')


def connect(path=None):
    """Connect to an SQLite database."""
    path = path if path else str(DB_FILE)
    cxn = sqlite3.connect(path)

    cxn.execute('PRAGMA page_size = {}'.format(2 ** 16))
    cxn.execute('PRAGMA busy_timeout = 10000')
    cxn.execute('PRAGMA journal_mode = WAL')
    return cxn


def create():
    """Create the database."""
    log(f'Creating database')

    script = fspath(SCRIPT_PATH / 'create_db.sql')
    cmd = f'sqlite3 {DB_FILE} < {script}'

    if DB_FILE.exists():
        remove(DB_FILE)

    subprocess.check_call(cmd, shell=True)


def backup_database():
    """Backup the SQLite3 database."""
    log('Backing up SQLite3 database')
    now = datetime.now()
    backup = f'{DB_FILE[:-3]}_{now.strftime("%Y-%m-%d")}.db'
    cmd = f'cp {DB_FILE} {backup}'
    subprocess.check_call(cmd, shell=True)
