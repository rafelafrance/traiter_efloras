"""Setup for all tests."""

from typing import Dict, List

from traiter.util import shorten

from efloras.pylib.pipeline import pipeline

NLP = pipeline()  # Singleton for testing


def test(text: str) -> List[Dict]:
    """Find entities in the doc."""
    text = shorten(text)

    doc = NLP(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits)

    # from spacy import displacy
    # options = {'collapse_punct': False, 'compact': True}
    # displacy.serve(doc, options=options)

    return traits
