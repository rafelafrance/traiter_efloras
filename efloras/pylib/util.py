"""Misc. utils."""
import csv
from datetime import datetime
from itertools import product

from ..pylib import const

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


def remove_traits(old_set: set, *remove: str) -> list:
    """Remove an element from a copy of the set."""
    removes = {r for r in remove}
    new_set = {e for e in old_set if e not in removes}
    return list(new_set)


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
