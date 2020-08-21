"""Build the NLP pipeline."""

from traiter.spacy_nlp import to_entities  # pylint: disable=import-error

from .nel import nel
from .util import ATTACH_STEP, TRAIT_STEP
from ..matchers.matcher import NLP

STEPS2ATTACH = {TRAIT_STEP, ATTACH_STEP}


def ner(text, link=True):
    """Find traits in the text and return a Doc()."""
    doc = NLP(text)

    if link:
        for sent in doc.sents:
            nel(sent)

    to_entities(doc, steps=STEPS2ATTACH)
    return doc


def trait_list(text):
    """Tests require a trait list."""
    doc = ner(text)

    traits = []

    for ent in doc.ents:
        data = ent._.data
        data['trait'] = ent.label_
        data['start'] = ent.start_char
        data['end'] = ent.end_char
        traits.append(data)

    # from pprint import pp
    # pp(traits)

    return traits
