"""Use a custom ruler to parse efloras pages."""

from collections import defaultdict

import pandas as pd
from bs4 import BeautifulSoup

import efloras.pylib.family_util as futil
from efloras.matchers.matcher import Matcher
from efloras.matchers.sentence import CONTAINS_TRAITS, SENT_STARTERS, \
    DESCRIPTOR, parse_sentences


def efloras_matcher(args, families):
    """Perform the parsing."""
    traits = set(args.trait)
    descriptor_traits = traits & DESCRIPTOR
    atomized_traits = traits - descriptor_traits

    descriptor_matcher = Matcher(descriptor_traits)
    sent_matcher = Matcher(atomized_traits)
    target_sents = {a for a, t in SENT_STARTERS.items() if t & traits}
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

            descriptor_traits = get_full_text_traits(
                descriptor_matcher, text)
            sent_traits, sents = get_sentence_traits(
                sent_matcher, target_sents, text)

            row['sentences'] = sents
            row = {**row, **descriptor_traits, **sent_traits}

            rows.append(row)

    df = pd.DataFrame(rows)
    return df


def get_full_text_traits(matcher, text):
    """Look for descriptor traits in the entire text."""
    traits = defaultdict(list)

    for label, data in matcher.parse(text).items():
        traits[label] += data

    return traits


def get_sentence_traits(matcher, target_sents, text):
    """Look for traits in the atoms."""
    traits = defaultdict(list)
    sents = []

    for sent in parse_sentences(text):
        if sent['value'] not in target_sents:
            continue
        sents.append(sent)
        sent_text = text[sent['start']:sent['end']]
        parses = matcher.parse(sent_text, sent['part'])
        for name, values in parses.items():
            for value in values:
                value['start'] += sent['start']
                value['end'] += sent['start']
            traits[name] += values

    return traits, sents


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
    for para in treatment.find_all('p'):
        text = ' '.join(para.get_text().split())
        if CONTAINS_TRAITS.search(text):
            return text
    return ''
