#!/usr/bin/env python

"""Migrate data from raw files to a database."""

import re

import pandas as pd

from src.pylib import family as futil
import src.pylib.db as db

INSERT = """
    insert into pages (flora_id, taxon_id, family, page_type, page_no, html)
        values (?, ?, ?, ?, ?, ?);
"""


def migrate_family_list():
    """As per the function name."""
    df = pd.read_csv(futil.FAMILY_DIR / 'eFloras_family_list.csv')
    cxn = db.connect()
    df.to_sql('families', cxn, index=None, if_exists='replace')

    sql = """
        create index families_key on families (flora_id, taxon_id);
        create index families_family on families (family);"""
    cxn.executescript(sql)


def create_pages_table():
    """As per the function name."""
    sql = """
    drop table if exists pages;
    create table pages (
        flora_id  integer,
        taxon_id  integer,
        family    text,
        page_type text,
        page_no   int,
        html      blob
    );
    create index pages_key on pages (flora_id, taxon_id);
    create index pages_fam on pages (flora_id, family);
    create index pages_type on pages (page_type);
    """
    with db.connect() as cxn:
        cxn.executescript(sql)


def migrate_home_page():
    """As per the function name."""
    home = futil.FAMILY_DIR / 'home_page.html'
    with open(home) as handle:
        html = handle.read()
    with db.connect() as cxn:
        flora_id = 0
        taxon_id = 0
        page_type = 'home'
        page_no = 1
        family = ''
        cxn.execute(
            INSERT, (flora_id, taxon_id, family, page_type, page_no, html))


def migrate_family_pages():
    """As per the function name."""
    with db.connect() as cxn:
        for page in futil.FAMILY_DIR.glob('flora_id*'):
            with open(page) as handle:
                html = handle.read()
            match = re.search(r'flora_id=(\d+)_page=(\d+)', str(page))
            flora_id, page_no = match.groups()
            taxon_id = 0
            page_type = 'families'
            family = ''
            cxn.execute(
                INSERT, (flora_id, taxon_id, family, page_type, page_no, html))


def migrate_tree_pages():
    """As per the function name."""
    with db.connect() as cxn:
        for page in futil.EFLORAS_DIR.glob('**/tree/*.html'):
            with open(page) as handle:
                html = handle.read()
            match = re.search(
                r'eFloras/([A-Za-z]+)_(\d+)/tree/taxon_id_(\d+)',
                str(page))
            family, flora_id, taxon_id = match.groups()
            page_type = 'tree'
            page_no = 1
            cxn.execute(
                INSERT, (flora_id, taxon_id, family, page_type, page_no, html))


def migrate_treatment_pages():
    """As per the function name."""
    with db.connect() as cxn:
        for page in futil.EFLORAS_DIR.glob('**/treatments/*.html'):
            with open(page) as handle:
                html = handle.read()
            match = re.search(
                r'eFloras/([A-Za-z]+)_(\d+)/treatments/taxon_id_(\d+)',
                str(page))
            family, flora_id, taxon_id = match.groups()
            page_type = 'treatment'
            page_no = 1
            cxn.execute(
                INSERT, (flora_id, taxon_id, family, page_type, page_no, html))


if __name__ == '__main__':
    """Do stuff."""
    # migrate_family_list()
    # create_pages_table()
    # migrate_home_page()
    # migrate_family_pages()
    # migrate_tree_pages()
    # migrate_treatment_pages()
