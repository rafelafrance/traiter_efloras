"""Common lobe count snippets."""

# from traiter.util import to_positive_int  # pylint: disable=import-error
#
# from .shared import RANGE_GROUPS
# from ..pylib.terms import REPLACE


def lobe(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    return data


LOBE = {
    'name': 'lobe',
    'on_match': lobe,
    'patterns': [
        [
        ],
    ],
}
