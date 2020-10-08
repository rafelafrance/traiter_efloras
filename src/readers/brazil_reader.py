"""Parse Brazil Flora html pages."""

import src.pylib.brazil_util as b_util
from bs4 import BeautifulSoup


def brazil_reader(args, families):
    """Parse the downloaded webpages."""
    rows = []
    for family in families:
        dir_ = b_util.BRAZIL_DIR / family
        for path in sorted(dir_.glob('*.html')):
            page = get_page(path)
            controlled = get_controlled(page)
            free = get_free(page)
            print('=' * 80)
            print(path)
            print()
            print(controlled)
            print()
            print(free)
            print()

    return rows


def get_page(path):
    """Get load the web page into memory."""
    with open(path) as in_file:
        page = in_file.read()
    page = BeautifulSoup(page, features='lxml')
    return page


def get_controlled(page):
    """Get the taxon description."""
    tag = page.select_one('.descricaoCamposControlados')
    tag = tag.select_one('table').get_text()
    return ' '.join(tag.split())


def get_free(page):
    """Get the taxon description."""
    tag = page.select_one('#tr-carregaTaxonGrupoDescricaoLivre')
    tag = tag.get_text()
    return ' '.join(tag.split())
