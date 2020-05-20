"""Use a custom ruler to parse efloras pages."""

from collections import defaultdict

import pandas as pd
from bs4 import BeautifulSoup

import efloras.pylib.family_util as futil
from efloras.matchers.matcher import Matcher
from efloras.pylib.atoms import ATOMIZER, ATOMS, DESCRIPTOR


def efloras_matcher(args, families):
    """Perform the parsing."""
    traits = set(args.trait)
    descriptor_traits = traits & DESCRIPTOR
    atomized_traits = traits - descriptor_traits

    descriptor_matcher = Matcher(descriptor_traits)
    atomized_matcher = Matcher(atomized_traits)
    target_atoms = {a for a, t in ATOMS.items() if t & traits}
    families_flora = futil.get_family_flora_ids(args, families)

    rows = []

    for family_name, flora_id in families_flora:
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

            flora_id = int(flora_id)
            atom_names = get_atom_names(text)

            descriptor_traits = get_descriptor_traits(
                descriptor_matcher, text)
            atomized_traits = get_atomized_traits(
                atomized_matcher, target_atoms, atom_names, text)

            row = {**row, **descriptor_traits, **atomized_traits}
            rows.append(row)

    df = pd.DataFrame(rows)
    return df


def get_descriptor_traits(matcher, text):
    """Look for descriptor traits in the entire text."""
    traits = defaultdict(list)

    for match in matcher.parse(text):
        for label, data in match.items():
            traits[label] += data

    return traits


def get_atomized_traits(matcher, target_atoms, atom_names, text):
    """Look for traits in the atoms."""
    traits = defaultdict(list)

    for i, (atom_start, name_end, atom_name) in enumerate(atom_names[:-1]):
        atom_name = atom_name.lower()
        text_end, *_ = atom_names[i + 1]
        atom_text = text[atom_start:text_end]

        if atom_name not in target_atoms:
            continue

        parses = matcher.parse(atom_text)
        for parse in parses:
            for label, data in parse.items():
                if label == 'part':
                    continue
                for datum in data:
                    datum['start'] += atom_start
                    datum['end'] += atom_start
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


def get_atom_names(text):
    """Break text into slices that are used to look for particular traits."""
    # The sections start with a keyword and extend up to the next keyword
    atoms = [(m.start(), m.end(), m.group(1)) for m in ATOMIZER.finditer(text)]
    atoms.append((-1, -1, ''))  # Sentinel
    return atoms


def get_treatment(path):
    """Get the taxon description page."""
    with open(path) as in_file:
        page = in_file.read()
    soup = BeautifulSoup(page, features='lxml')
    return soup.find(id='panelTaxonTreatment')


def get_traits(treatment):
    """Find the trait paragraph in the treatment."""
    for para in treatment.find_all('p'):
        text = ' '.join(para.get_text().split())
        if ATOMIZER.search(text):
            return text
    return ''
