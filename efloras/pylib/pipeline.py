"""Build the NLP pipeline."""

from collections import defaultdict

from traiter.spacy_nlp import spacy_nlp  # pylint: disable=import-error

from .sentencizer import custom_sentencizer
from ..matchers.matcher import Matcher
from ..pylib.attach_fsm import attach_traits_to_parts
from ..pylib.util import STEPS2ATTACH

NLP = spacy_nlp(disable=['ner'])
NLP.add_pipe(custom_sentencizer, before='parser')

MATCHER = Matcher(NLP)
NLP.add_pipe(MATCHER, after='parser')


def parse(text, with_sents=False, attach=True):
    """Parse the traits."""
    doc = NLP(text)

    traits = defaultdict(list)

    sents = []

    for sent in doc.sents:
        sents.append((sent.start_char, sent.end_char))

        if attach:
            attach_traits_to_parts(sent)

    for token in doc:
        if (token._.step in STEPS2ATTACH and token._.data
                and not token._.aux.get('skip')):
            data = {k: v for k, v in token._.data.items()
                    if not k.startswith('_')}
            data['start'] = token.idx
            data['end'] = token.idx + len(token)
            traits[token.ent_type_].append(data)

    # from pprint import pp
    # pp(dict(traits))

    return (traits, sents) if with_sents else traits
