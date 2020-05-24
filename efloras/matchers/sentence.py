"""List all of the matchers."""

import nltk
from nltk.tokenize import TreebankWordTokenizer
import regex
from traiter.util import FLAGS


DESCRIPTOR = set(""" seasonal_descriptor sexual_descriptor symmetry_descriptor
    temporal_descriptor """.split())
CALYX = {'calyx_size', 'caylx_shape', 'caylx_color'}
COROLLA = {'corolla_size', 'corolla_shape', 'corolla_color'}
FLOWER = {'flower_shape', 'flower_size', 'flower_color'}
FRUIT = {'fruit_shape', 'fruit_size', 'fruit_color'}
HYPANTHIUM = {'hypanthium_shape', 'hypanthium_size', 'hypanthium_color'}
LEAF = {'leaf_size', 'leaf_shape'}
PETAL = {'petal_size', 'petal_shape', 'petal_color'}
PETIOLE = {'petiole_size', 'petiole_shape'}
SEED = {'seed_size'}
SEPAL = {'sepal_size', 'sepal_shape', 'sepal_color'}


# Keywords used to split treatment into text sentences
SENT_STARTERS = {
    'basal leaves': LEAF,
    'capsule': FRUIT,
    'cauline leaves': LEAF,
    'corollas': COROLLA,
    'flowering': FLOWER,
    'flowering stems': FLOWER,
    'flowers': FLOWER,
    'fruits': FRUIT,
    'hypanthia': HYPANTHIUM,
    # 'inflorescences': FLOWER,
    # 'inflorescenses': FLOWER,
    'leaf blade': LEAF,
    'leaf blades': LEAF,
    'leaflets': LEAF,
    'leaves': LEAF,
    'pepos': FRUIT,
    'petals': PETAL,
    'petioles': PETIOLE,
    'pistillate corollas': COROLLA,
    'pistillate flowers': FLOWER,
    # 'pistillate inflorescences': FLOWER,
    'pistillate racemes': FLOWER,
    'racemes': FLOWER,
    'seeds': SEED,
    'staminate corollas': COROLLA,
    'staminate flowers': FLOWER,
    # 'staminate inflorescences': FLOWER,
    'staminate racemes': FLOWER,
    'stem leaves': LEAF,
}

# TODO: This may not work for every situation
PARTS = {k: next(iter(v)).split('_')[0] for k, v in SENT_STARTERS.items()}


ABBREVS = """ ca vs inc i.e fl fr diam d.b.h mm cm m M var vars gaz syst
        comm cit loc pers sq subsp subspp illeg
        Gard Bull
        Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
        """.split()
SENTENCE_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')
SENTENCE_TOKENIZER._params.abbrev_types.update(ABBREVS)

CONTAINS_TRAITS = sorted(
    SENT_STARTERS.keys(), reverse=True, key=lambda s: len(s))
CONTAINS_TRAITS = ' | '.join(
    r' \s '.join(x.split()) for x in CONTAINS_TRAITS)
# ATOMIZER = regex.compile(
#     rf""" (?<! [\w:,<>()] \s) \b ( {ATOMIZER} ) \b  """, flags=FLAGS)
CONTAINS_TRAITS = regex.compile(
    rf""" (?<= ^ \s* | [.] \s* ) \b ( {CONTAINS_TRAITS} ) \b  """, flags=FLAGS)


SPAN_TOKENIZER = TreebankWordTokenizer()


def parse_sentences(text):
    """Break the text into atoms."""
    sents = []

    for start, end in SENTENCE_TOKENIZER.span_tokenize(text):
        sentence = text[start:end]
        tokens = nltk.word_tokenize(sentence)
        spans = list(SPAN_TOKENIZER.span_tokenize(sentence))

        value = ''

        if (len(tokens) >= 2 and
                (value := ' '.join(tokens[:2]).lower()) in SENT_STARTERS):
            sents.append({
                'value': value,
                'start': start,
                'end': end,
                'leader_start': spans[0][0] + start,
                'leader_end': spans[1][1] + start,
                'part': PARTS[value],
            })

        elif (len(tokens) >= 1
              and (value := tokens[0].lower()) in SENT_STARTERS):
            sents.append({
                'value': value,
                'start': start,
                'end': end,
                'leader_start': spans[0][0] + start,
                'leader_end': spans[0][1] + start,
                'part': PARTS[value],
            })

    return sents
