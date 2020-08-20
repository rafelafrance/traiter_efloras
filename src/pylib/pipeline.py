"""Build the NLP pipeline."""

# pylint: disable=import-error
from traiter.spacy_nlp import spacy_nlp, to_entities

from .sentencizer import custom_sentencizer
from ..matchers.matcher import Matcher
from ..pylib.nel import nel
from ..pylib.util import STEPS2ATTACH

NLP = spacy_nlp(disable=['ner'])
NLP.add_pipe(custom_sentencizer, before='parser')

MATCHER = Matcher(NLP)
NLP.add_pipe(MATCHER, after='parser')


def parse(text, with_sents=False, attach=True):
    """Parse the traits."""
    doc = NLP(text)

    traits = []

    if attach:
        for sent in doc.sents:
            nel(sent)

    for token in doc:
        if (token._.step in STEPS2ATTACH and token._.data
                and not token._.data.get('_skip')):
            data = {k: v for k, v in token._.data.items()
                    if not k.startswith('_')}
            data['trait'] = token.ent_type_
            data['start'] = token.idx
            data['end'] = token.idx + len(token)
            traits.append(data)

    # from pprint import pp
    # pp(traits)

    sents = []
    if with_sents:
        sents = [(s.start_char, s.end_char) for s in doc.sents]

    return (traits, sents) if with_sents else traits


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
