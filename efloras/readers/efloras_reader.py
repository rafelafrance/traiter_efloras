"""Use a custom ruler to parse efloras pages."""

from collections import defaultdict

import pandas as pd
from bs4 import BeautifulSoup

import efloras.pylib.family_util as futil
from efloras.matchers.matcher import Matcher
from efloras.matchers.plant_part import PATTERN_RE


def efloras_reader(args, families):
    """Perform the parsing."""
    matcher = Matcher()
    families_flora = futil.get_family_flora_ids(args, families)

    rows = []

    for family_name, flora_id in families_flora:
        flora_id = int(flora_id)
        family = families[(family_name, flora_id)]
        taxa = get_family_tree(family)
        root = futil.treatment_dir(flora_id, family['family'])
        for i, path in enumerate(root.glob('*.html')):
            treatment = get_treatment(path)
            text = get_traits(treatment)
            taxon_id = futil.get_taxon_id(path)

            row = {
                'family': family['family'],
                'flora_id': flora_id,
                'taxon': taxa[taxon_id],
                'taxon_id': taxon_id,
                'link': futil.treatment_link(flora_id, taxon_id),
                'text': '',
            }

            if text is None:
                rows.append(row)
                continue

            row['text'] = text

            traits = match_traits(matcher, text)

            row = {**row, **traits}

            rows.append(row)

    df = pd.DataFrame(rows)
    return df


def match_traits(matcher, text):
    """Look for descriptor traits in the entire text."""
    traits = defaultdict(list)

    for part in matcher.parse(text):
        for label, data in part.items():
            traits[label] += data

    return traits


def get_family_tree(family):
    """Get all taxa for the all of the families."""
    taxa = {}
    tree_dir = futil.tree_dir(family['flora_id'], family['family'])
    for path in tree_dir.glob('*.html'):

        with open(path) as in_file:
            page = in_file.read()

        soup = BeautifulSoup(page, features='lxml')

        for link in soup.findAll('a', attrs={'title': futil.TAXON_RE}):
            href = link.attrs['href']
            taxon_id = futil.get_taxon_id(href)
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
        unique = {m for m in PATTERN_RE.findall(text)}
        if len(unique) > high:
            best = text
            high = len(unique)
        if high > 3:
            return best
    return best
