"""Read pages scraped from the eFloras website."""

import sys
from collections import defaultdict
import regex
from lxml import html
from lxml.etree import tostring
import pandas as pd
import efloras.pylib.db as db
import efloras.pylib.util as util
import efloras.pylib.trait_groups as tg

TAXON_SEEN = {}
VALID_TAXON = set()
TAXON_RANKS = set()


def efloras_reader(args, families):
    """Parse all pages for the given families."""
    get_valid_taxa()
    get_taxon_ranks()
    rows = []
    for family in args.family:
        name = families[family]['family']
        root = util.DATA_DIR / f'{name}_{args.flora_id}'
        for path in root.glob('**/*.html'):
            row = parse_efloras_page(args, path, family)
            rows.append(row)
    df = pd.DataFrame(rows)
    return df


def get_valid_taxa():
    """Get valid taxa names."""
    global VALID_TAXON
    with db.connect() as cxn:
        VALID_TAXON = {n
                       for t in db.select_taxa(cxn)
                       for n in t[0].lower().split()}


def get_taxon_ranks():
    """Get taxon ranks."""
    global TAXON_RANKS
    with db.connect() as cxn:
        TAXON_RANKS = {r[0].lower() for r in db.select_taxon_names(cxn)}
    TAXON_RANKS.add('subfam.')
    TAXON_RANKS.add('sect.')
    TAXON_RANKS.add('×')
    TAXON_RANKS.add('x')


def parse_efloras_page(args, path, family):
    """Parse the taxon page."""
    page = get_efloras_page(path)
    taxon = get_taxon(page)
    check_taxon(taxon, path)

    row = {
        'family': family,
        'taxon': taxon,
        'path': str(path),
        'text': ''}

    para, text = find_trait_groups_paragraph(page)
    if para is not None:
        check_trait_groups(para)
        row['text'] = text
        row = {**row, **parse_traits(args, text)}
    return row


def check_taxon(taxon, path):
    """Make sure the taxon parse is reasonable."""
    if taxon in TAXON_SEEN:
        print(f'Taxon "{taxon}" in both {TAXON_SEEN[taxon]} & {path}')
        sys.exit()
    TAXON_SEEN[taxon] = path


def get_efloras_page(path):
    """Get the taxon description page."""
    with open(path) as in_file:
        page = in_file.read()
    return html.fromstring(page)


# TODO: Move this logic to a new-style trait parser
def get_taxon(page):
    """Get the taxon description."""
    taxon_id = 'lblTaxonDesc'
    # taxon = page.xpath(f'//*[@id="{taxon_id}"]/b/text()')
    frag = page.xpath(f'//*[@id="{taxon_id}"]')[0]
    match = regex.match(b'(.*?)<p>', tostring(frag), flags=regex.DOTALL)
    words = match.group(1).decode() + '</span>'
    words = html.fromstring(words).text_content().split()
    taxon = []
    next_word = False
    for word in words:
        word = regex.sub(
            r'\p{Open_Punctuation}|\p{Close_Punctuation}', '', word)
        norm = word.lower()
        if next_word:
            taxon.append(word)
            next_word = False
        elif norm in TAXON_RANKS:
            next_word = True
        elif norm in VALID_TAXON:
            taxon.append(word)
        elif norm[0] in ('×', ):
            taxon.append(word)

    taxon = ' '.join(taxon)
    return taxon


def find_trait_groups_paragraph(page):
    """Scan the page for the traits paragraph."""
    treatment_id = 'panelTaxonTreatment'  # HTML ID of the plant treatment

    # Find the general area on the page with the trait groups
    paras = page.xpath(f'//*[@id="{treatment_id}"]//p')

    for para in paras:
        text = ' '.join(para.text_content().split())
        match = tg.TRAIT_GROUPS_RE.search(text)
        if match:
            return para, text

    return None, None


def check_trait_groups(para):  # , text):
    """Validate that we have all of the traits."""
    bold = para.xpath('.//b')  # Used to check the trait group parse

    # We are just using the bold items as a check on the trait groups
    bolds = [regex.sub('[:.,]', '', x.text_content()) for x in bold]
    bolds = [x.strip().lower() for x in bolds if x]

    # Fewer trait groups than bold items means something is wrong
    if set(bolds) > set(tg.TRAIT_GROUPS.keys()):
        diff = set(bolds) - set(tg.TRAIT_GROUPS.keys())
        sys.exit(f'Found new trait group: {diff}')


def parse_traits(args, text):
    """Parse each trait."""
    traits = defaultdict(list)

    arg_traits = set(args.trait)

    # Find the sections of text that may hold traits. The sections start with
    # a keyword and extend up to the next keyword.
    slices = [(m.start(), m.end()) for m in tg.TRAIT_GROUPS_RE.finditer(text)]
    slices.append((-1, -1))

    # Loop over all of the sections
    for i, (start, end) in enumerate(slices[:-1]):
        after, _ = slices[i + 1]
        trait_name = text[start:end].lower()
        group_data = text[start:after]

        # Certain traits are associated with each keyword. We want to get the
        # intersection of the user selected traits with that section.
        parsers = {t for t in tg.TRAIT_GROUPS.get(trait_name)
                   if t.name in arg_traits}

        # Now we parse all of the intersecting traits
        for parser in parsers:
            parses = parser.parse(group_data)
            if parses:
                for parse in parses:
                    setattr(parse, 'trait_group', trait_name)
                    parse.start += start
                    parse.end += start
                traits[parser.name] += parses
    return traits
