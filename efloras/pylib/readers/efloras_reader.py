import re
from dataclasses import dataclass
from dataclasses import field

from bs4 import BeautifulSoup
from plants.patterns.term_patterns import PARTS_SET
from plants.patterns.term_patterns import TERMS
from tqdm import tqdm
from traiter.const import FLAGS

from .. import util

TAXON_TITLE = "Accepted Name"


@dataclass
class EflorasRow:
    family: str
    flora_id: int
    flora_name: str
    taxon: str
    taxon_id: int
    link: str
    path: str
    text: str
    traits: list = field(default_factory=list)


# Used to filter paragraphs in the source documents.
PARA_RE = sorted(
    " ".join(t["pattern"].split()) for t in TERMS if t["label"] in PARTS_SET
)
PARA_RE = f"({'|'.join(PARA_RE)})"
PARA_RE = re.compile(PARA_RE, flags=re.IGNORECASE)


def reader(args, families):
    """Perform the parsing."""
    families_flora = util.get_family_flora_ids(args, families)
    flora_ids = util.get_flora_ids()

    # Build a filter for the taxon names
    genera = [g.lower() for g in args.genus] if args.genus else []
    genera = [r"\s".join(g.split()) for g in genera]
    genera = "|".join(genera)

    rows = []

    for family_name, flora_id in tqdm(families_flora):
        flora_id = int(flora_id)
        family = families[(family_name, flora_id)]
        taxa = get_family_tree(family)
        root = util.treatment_dir(flora_id, family["family"])
        for path in root.glob("*.html"):
            text = get_treatment(path)
            text = get_traits_para(text)
            taxon_id = util.get_taxon_id(path)

            # Must have a taxon name
            if not taxa.get(taxon_id):
                continue

            # Filter on the taxon name
            if genera and not re.search(genera, taxa[taxon_id], flags=FLAGS):
                continue

            rows.append(
                EflorasRow(
                    family=family["family"],
                    flora_id=flora_id,
                    flora_name=flora_ids[flora_id],
                    taxon=taxa[taxon_id],
                    taxon_id=taxon_id,
                    link=treatment_link(flora_id, taxon_id),
                    path=path,
                    text=text if text else "",
                )
            )

    return rows


def get_family_tree(family):
    """Get all taxa for the all the families."""
    taxa = {}
    tree_dir = util.tree_dir(family["flora_id"], family["family"])
    for path in tree_dir.glob("*.html"):
        with open(path) as in_file:
            page = in_file.read()

        soup = BeautifulSoup(page, features="lxml")

        for link in soup.findAll("a", attrs={"title": TAXON_TITLE}):
            href = link.attrs["href"]
            taxon_id = util.get_taxon_id(href)
            taxa[taxon_id] = link.text

    return taxa


def get_treatment(path):
    """Get the taxon description page."""
    with open(path) as in_file:
        page = in_file.read()
    soup = BeautifulSoup(page, features="lxml")
    return soup.find(id="panelTaxonTreatment")


def get_traits_para(treatment):
    """Find the trait paragraph in the treatment."""
    if not treatment:
        return ""
    best = ""
    high = 0
    for para in treatment.find_all("p"):
        text = " ".join(para.get_text().split())
        unique = set(PARA_RE.findall(text))
        if len(unique) > high:
            best = " ".join(para.get_text().split())
            high = len(unique)
        if high >= 5:
            return best
    return best if high >= 4 else ""


def treatment_link(flora_id, taxon_id):
    """Build a link to the treatment page."""
    return (
        "http://www.efloras.org/florataxon.aspx?"
        rf"flora_id={flora_id}&taxon_id={taxon_id}"
    )
