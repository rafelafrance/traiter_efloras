"""Use a custom ruler to parse efloras pages."""

# import sys
from collections import defaultdict

import pandas as pd
from bs4 import BeautifulSoup

import efloras.pylib.family_util as futil
import efloras.pylib.util as util
from efloras.matchers.all import MATCHERS


def efloras_ruler(args, families):
    """Perform the parsing."""
    combos = futil.get_family_flora_ids(args, families)
    rows = []
    for key in combos:
        family = families[key]
        name = family['family']
        flora_id = family['flora_id']
        root = util.DATA_DIR / 'treatments' / f'{name}_{flora_id}'
        for path in root.glob('**/*.html'):
            row = parse_efloras_page(args, path, family)
            rows.append(row)
    df = pd.DataFrame(rows)
    return df


def parse_efloras_page(args, path, family):
    """Parse the taxon treatment."""
    treatment = get_treatment(path)
    text = get_traits(treatment)
    taxon = ''  # get_taxon()

    row = {
        'family': family['family'],
        'flora_id': int(family['flora_id']),
        'taxon': taxon,
        'path': str(path),
        'text': ''}

    if text is None:
        return row

    row['text'] = text

    atoms = find_atom_names(text)
    # check_trait_groups(atoms)

    row = {**row, **parse_traits(args, atoms, text)}

    return row


def parse_traits(args, atoms, text):
    """Look for traits in the atoms."""
    traits = defaultdict(list)
    arg_traits = set(args.trait)

    for i, (atom_start, name_end) in enumerate(atoms[:-1]):
        text_end, _ = atoms[i + 1]
        atom_name = text[atom_start:name_end].lower()
        atom_text = text[atom_start:text_end]

        # Certain traits are associated with each atom keyword. We want the
        # intersection of traits arguments with what may be in an atom
        rulers = {t for t in MATCHERS.get(atom_name)
                  if t.name in arg_traits}

        # Now parse all of the intersecting traits
        for ruler in rulers:
            entities = ruler.extract(atom_text)
            for entity in entities:
                setattr(entity, 'trait_group', atom_name)
                entity.start += atom_start
                entity.end += atom_start
            # traits[entity.name] += entity

    return traits


def find_atom_names(text):
    """Break text into slices that are used to look for particular traits."""
    # The sections start with a keyword and extend up to the next keyword
    atoms = [(m.start(), m.end()) for m in MATCHERS.finditer(text)]
    atoms.append((-1, -1))  # Sentinel
    return atoms


def get_treatment(path):
    """Get the taxon description page."""
    with open(path) as in_file:
        page = in_file.read()
    soup = BeautifulSoup(page, features='lxml')
    treatment = soup.find(id='panelTaxonTreatment')
    return treatment


def get_traits(treatment):
    """Find the traits paragraph on the page."""
    for para in treatment.select('p'):
        text = para.get_text(strip=True)
        match = MATCHERS.RULER_GROUPS_RE.search(text)
        if match:
            return text
    return None
