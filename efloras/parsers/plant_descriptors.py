"""Plant descriptors."""

from typing import Any

from traiter.token import Token
from traiter.vocabulary import Vocabulary

import efloras.pylib.shared_patterns as patterns
from efloras.parsers.base import Base
from efloras.pylib.trait import Trait

VOCAB = Vocabulary(patterns.VOCAB)

VOCAB.term('sexual_descriptor', r"""
    androdioecious
    bisexual
    dioecious
    gynodioecious
    hermaphroditic
    monoecious
    perfect protandrous protogynous
    unisexual
    """.split())

VOCAB.term('symmetry_descriptor', r"""
    Actinomorphic
    Zygomorphic
    """.split())


def convert(token: Token) -> Any:
    """Convert parsed token into a trait."""
    trait = Trait(
        start=token.start, end=token.end,
        value=token.group['value'])
    return trait


def parser(descriptor):
    """Build a parser for the flower part."""
    catalog = Vocabulary(VOCAB)
    return Base(
        name=f'{descriptor}',
        rules=[
            catalog.producer(convert, f""" (?P<value> {descriptor} ) """),
        ],
    )


SEXUAL_DESCRIPTOR = parser('sexual_descriptor')
SYMMETRY_DESCRIPTOR = parser('symmetry_descriptor')
