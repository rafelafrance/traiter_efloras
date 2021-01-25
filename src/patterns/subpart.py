"""Plant subpart parser."""

import spacy
from traiter.pipes.entity_data import text_action

from ..pylib.consts import REPLACE

SUBPART = [
    {
        'label': 'subpart',
        'on_match': 'subpart.v1',
        'patterns': [[
            {'ENT_TYPE': 'subpart'},
        ]],
    },
]


@spacy.registry.misc(SUBPART[0]['on_match'])
def subpart(ent):
    """Enrich a plant subpart match."""
    text_action(ent, REPLACE)
