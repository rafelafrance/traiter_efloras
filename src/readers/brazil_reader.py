"""Parse Brazil Flora html pages."""

import json
import src.pylib.brazil_util as b_util
from bs4 import BeautifulSoup


def brazil_reader(_, families):
    """Parse the downloaded webpages."""
    rows = []
    for family in families:
        dir_ = b_util.BRAZIL_DIR / family
        links = get_species(family)
        for path in sorted(dir_.glob('*.html')):
            page = get_page(path)
            controlled = get_controlled(page)
            free = get_free(page)
            taxon_id = get_taxon_id(page)
            row = {
                'family': family,
                'taxon': path.stem.replace('_', ' '),
                'text': controlled,
                'free': free,
                'link': links.get(taxon_id, ''),
            }
            rows.append(row)
    return rows


def get_species(family):
    """Get the species data."""
    path = b_util.species_path(family)
    with open(path) as json_file:
        data = json.load(json_file)
    return {d['taxonid']: d['references'] for d in data['result']}


def get_taxon_id(page):
    """Get the taxon ID from the page."""
    taxon_id = page.select_one('#carregaTaxonGrupoIdDadosListaBrasil')
    taxon_id = taxon_id['value']
    return taxon_id


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
