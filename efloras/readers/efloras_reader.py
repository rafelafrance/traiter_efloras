"""Use a custom ruler to parse efloras pages."""

from collections import defaultdict

import pandas as pd
from bs4 import BeautifulSoup

import efloras.pylib.family_util as futil
from efloras.pylib.atoms import ATOMIZER
from efloras.pylib.traits import TRAIT_NAMES


def efloras_matcher(args, families):
    """Perform the parsing."""
    combos = futil.get_family_flora_ids(args, families)
    rows = []
    for key in combos:
        family = families[key]
        taxa = get_family_tree(family)
        name = family['family']
        flora_id = family['flora_id']
        root = futil.treatment_dir(flora_id, name)
        for path in root.glob('*.html'):
            row = parse_treatment_page(args, path, family, taxa)
            rows.append(row)
    df = pd.DataFrame(rows)
    flora_ids = futil.get_flora_ids()
    df['flora_name'] = df['flora_id'].apply(lambda f: flora_ids[f])
    return df


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


def parse_treatment_page(args, path, family, taxa):
    """Parse the taxon treatment."""
    treatment = get_treatment(path)
    text = get_traits(treatment)
    flora_id = int(family['flora_id'])
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
        return row

    row['text'] = text

    atoms = find_atom_names(text)

    row = {**row, **extract_traits(args, atoms, text)}

    return row


def extract_traits(args, atoms, text):
    """Look for traits in the atoms."""
    traits = defaultdict(list)
    arg_traits = set(args.trait)

    for i, (atom_start, name_end) in enumerate(atoms[:-1]):
        text_end, _ = atoms[i + 1]
        atom_name = text[atom_start:name_end].lower()
        atom_text = text[atom_start:text_end]

        # Certain traits are associated with each atom keyword. We want the
        # intersection of traits arguments with what may be in an atom
        trait_names = {t for t in atoms.ATOMS.get(atom_name)
                       if t in arg_traits}

        # Now parse all of the intersecting traits
        for trait_name in trait_names:
            matcher = TRAIT_NAMES[trait_name]
            for trait in matcher.parse(atom_text):
                trait.start += atom_start
                trait.end += atom_start
                traits[trait_name].append(trait)

    return traits


def find_atom_names(text):
    """Break text into slices that are used to look for particular traits."""
    # The sections start with a keyword and extend up to the next keyword
    atoms = [(m.start(), m.end()) for m in ATOMIZER.finditer(text)]
    atoms.append((-1, -1))  # Sentinel
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
