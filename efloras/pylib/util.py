import csv
import re
from datetime import datetime
from itertools import product

from . import const

CONVERT = {
    "cm": 10.0,
    "dm": 100.0,
    "m": 1000.0,
    "mm": 1.0,
    "µm": 1.0e-3,
    "centimeters": 10.0,
    "decimeters": 100.0,
    "meters": 1000.0,
    "millimeters": 1.0,
}


def convert(number, units):
    """Normalize the units to meters."""
    return number * CONVERT.get(units, 1.0)


def get_families():
    """Get a list of all families in the eFloras catalog."""
    families = {}

    with open(const.EFLORAS_FAMILIES) as in_file:

        for family in csv.DictReader(in_file):

            times = {"created": "", "modified": "", "count": 0}

            path = (
                const.DATA_DIR / "eFloras" / f"{family['family']}_{family['flora_id']}"
            )

            if path.exists():
                times["count"] = len(list(path.glob("**/treatments/*.html")))
                if times["count"]:
                    stat = path.stat()
                    times["created"] = datetime.fromtimestamp(stat.st_ctime).strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    times["modified"] = datetime.fromtimestamp(stat.st_mtime).strftime(
                        "%Y-%m-%d %H:%M"
                    )

            key = (family["family"].lower(), int(family["flora_id"]))
            families[key] = {**family, **times}

    return families


def get_flora_ids():
    """Get a list of flora IDs."""
    flora_ids = {}
    with open(const.EFLORAS_FAMILIES) as in_file:
        for family in csv.DictReader(in_file):
            flora_ids[int(family["flora_id"])] = family["flora_name"]
    return flora_ids


def get_family_flora_ids(args, families):
    """Get family and flora ID combinations."""
    return [c for c in product(args.family, args.flora_id) if c in families]


def get_taxon_id(href):
    """Given a link or file name return a taxon ID."""
    href = str(href)
    taxon_id_re = re.compile(r"taxon_id[=_](\d+)")
    return int(taxon_id_re.search(href)[1])


def treatment_dir(flora_id, family_name):
    return family_dir(flora_id, family_name) / "treatments"


def tree_dir(flora_id, family_name):
    return family_dir(flora_id, family_name) / "tree"


def family_dir(flora_id, family_name):
    """Build the family directory name."""
    taxon_dir = f"{family_name}_{flora_id}"
    return const.DATA_DIR / "eFloras" / taxon_dir
