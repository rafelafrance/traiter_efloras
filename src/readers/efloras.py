"""Parse eFloras html pages."""

import re

from bs4 import BeautifulSoup
from traiter.util import FLAGS  # pylint: disable=import-error

import downloader
import extract
import src.pylib.util as util
from src.matchers.part import PATTERN_RE

_TAXON_RE = re.compile(r'Accepted Name', flags=re.IGNORECASE)


def efloras_reader(args, families):
    """Perform the parsing."""
    families_flora = extract.get_family_flora_ids(args, families)
    flora_ids = util.get_flora_ids()

    # Build a filter for the taxon names
    genera = [g.lower() for g in args.genus] if args.genus else []
    genera = [r'\s'.join(g.split()) for g in genera]
    genera = '|'.join(genera)

    rows = []

    for family_name, flora_id in families_flora:
        flora_id = int(flora_id)
        family = families[(family_name, flora_id)]
        taxa = get_family_tree(family)
        root = downloader.treatment_dir(flora_id, family['family'])
        for path in root.glob('*.html'):
            text = get_treatment(path)
            text = get_traits(text)
            taxon_id = downloader.get_taxon_id(path)
            if not taxa.get(taxon_id):
                continue

            # Filter on the taxon name
            if genera and not re.search(genera, taxa[taxon_id], flags=FLAGS):
                continue

            row = {
                'family': family['family'],
                'flora_id': flora_id,
                'flora_name': flora_ids[flora_id],
                'taxon': taxa[taxon_id],
                'taxon_id': taxon_id,
                'link': treatment_link(flora_id, taxon_id),
                'text': '',
                'traits': {},
            }

            if text is None:
                rows.append(row)
                continue

            row['text'] = text
            rows.append(row)

    return rows


def get_family_tree(family):
    """Get all taxa for the all of the families."""
    taxa = {}
    tree_dir = downloader.tree_dir(family['flora_id'], family['family'])
    for path in tree_dir.glob('*.html'):

        with open(path) as in_file:
            page = in_file.read()

        soup = BeautifulSoup(page, features='lxml')

        for link in soup.findAll('a', attrs={'title': _TAXON_RE}):
            href = link.attrs['href']
            taxon_id = downloader.get_taxon_id(href)
            taxa[taxon_id] = link.text

    return taxa


def get_treatment(path):
    """Get the taxon description page."""
    with open(path) as in_file:
        page = in_file.read()
    soup = BeautifulSoup(page, features='lxml')
    return soup.find(id='panelTaxonTreatment')


def get_traits(treatment):
    """Find the trait paragraph in the treatment."""
    if not treatment:
        return ''
    best = ''
    high = 0
    for para in treatment.find_all('p'):
        text = ' '.join(para.get_text().split())
        unique = set(PATTERN_RE.findall(text))
        if len(unique) > high:
            best = text
            high = len(unique)
        if high >= 5:
            return best
    return best if high >= 5 else ''


def treatment_link(flora_id, taxon_id):
    """Build a link to the treatment page."""
    return ('http://www.efloras.org/florataxon.aspx?'
            rf'flora_id={flora_id}&taxon_id={taxon_id}')
