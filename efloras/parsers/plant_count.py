"""Parse the trait."""

from typing import Any

from traiter.token import Token
from traiter.vocabulary import Vocabulary

import efloras.pylib.shared_patterns as patterns
from efloras.parsers.base import Base
from efloras.pylib.trait import Trait


def convert(token: Token) -> Any:
    """Convert parsed token into a trait."""
    trait = Trait(start=token.start, end=token.end)

    if 'location' in token.group:
        trait.location = token.group['location'].lower()

    if 'part' in token.group:
        trait.part = token.group['part'].lower()

    for key in ['min', 'low', 'high', 'max']:
        if key in token.group:
            setattr(trait, key, float(token.group[key]))

    return trait


def parser(plant_part):
    """Build a parser for the flower part."""
    catalog = Vocabulary(patterns.VOCAB)
    return Base(
        name=f'{plant_part}_count',
        rules=[
            catalog[plant_part],
            catalog['plant_part'],
            catalog.term('skip', r""" locular [/] """.split()),

            catalog.producer(convert, f"""
                (?P<part> {plant_part} ) (word | skip)*
                ( count_upper | range )
                (?! units | cross_joiner | skip )
                """),
        ],
    )


SEPAL_COUNT = parser('sepal')
