"""Shared plant parser logic."""

import regex
from traiter.vocabulary import Vocabulary, FIRST, LOWEST
from efloras.pylib import util

VOCAB = Vocabulary()


# Chars that may be a token
VOCAB.part('slash', r' [/] ', capture=False)
VOCAB.part('dash', r' \p{Pd} ', capture=False)
VOCAB.part('open', r' \p{Ps} ', capture=False)
VOCAB.part('close', r' \p{Pe} ', capture=False)
VOCAB.part('x', r' [x×] ', capture=False)
VOCAB.part('quest', r' [?] ')
VOCAB.part('comma', r' [,] ', capture=False, priority=LOWEST)
VOCAB.part('semicolon', r' [;] ', capture=False, priority=LOWEST)
VOCAB.part('ampersand', r' [&] ', capture=False)
VOCAB.part('eq', r' [=] ', capture=False)
VOCAB.part('under', r' [_] ', capture=False)
VOCAB.part('eol', r' [\n\r\f] ', capture=False)
VOCAB.part('dot', r' [.] ', capture=False)

# Small words
VOCAB.part('by', r' by ', capture=False)
VOCAB.part('to', r' to ', capture=False)
VOCAB.part('with', r' with ', capture=False)
VOCAB.part('up_to', r' ( up \s+ )? to ', capture=False)
VOCAB.term('and', r' and ', capture=False)
VOCAB.term('conj', ' or and '.split(), capture=False)
VOCAB.term('prep', ' to with on of '.split(), capture=False)

# NOTE: Double quotes as inches is handled elsewhere
VOCAB.part('inches', r"""
    (?<! [a-z] ) ( inch e? s? | in s? (?! [a-ru-wyz] ) ) """)
VOCAB.part('feet', r"""
    (?<! [a-z] ) ( foot s? | feet s? | ft s? (?! [,\w]) ) | (?<= \d ) ' """)
VOCAB.part('metric_len', r"""
    ( milli | centi )? meters? | ( [cm] [\s.]? m ) (?! [a-ru-wyz] ) """)
VOCAB.grouper('len_units', ' metric_len feet inches'.split())

VOCAB.part('pounds', r' pounds? | lbs? ')
VOCAB.part('ounces', r' ounces? | ozs? ')
METRIC_MASS = r"""
    milligrams? | kilograms? | grams?
    | (?<! [a-z] )( m \.? g s? | k \.? \s? g a? | g[mr]? s? )(?! [a-z] )
    """
VOCAB.part('metric_mass', METRIC_MASS)
VOCAB.grouper('mass_units', 'metric_mass pounds ounces'.split())

VOCAB.grouper('us_units', 'feet inches pounds ounces'.split())
VOCAB.grouper('units', 'len_units mass_units'.split())

# # UUIDs cause problems when extracting certain shorthand notations.
VOCAB.part('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """,
           capture=False, priority=FIRST)

# Some numeric values are reported as ordinals or words
ORDINALS = [util.ordinal(x) for x in range(1, 6)]
VOCAB.part('ordinals', [util.number_to_words(x) for x in ORDINALS])

# Time units
VOCAB.part('time_units', r'years? | months? | weeks? | days? | hours?')

# Integers, no commas or signs and typically small
VOCAB.part('integer', r""" \d+ (?! [%\d\-] ) """)

# Date
VOCAB.part('month_name', """
    (?<! [a-z])
    (?P<month>
        january | february | march | april | may | june | july | august
        | september | october | november | december
        | jan | feb | mar | apr | jun | jul | aug | sept? | oct | nov | dec
    )
    (?! [a-z] )
    """, capture=False)


SEX = r'staminate | pistillate'
VOCAB.term('sex', SEX)

VOCAB.term('plant_part', r"""
    (?<! to \s )
    ( androeci(a|um) | anthers?
    | blades?
    | caly(ces|x) | carpels? | corollas?
    | flowers?
    | gynoeci(a|um)
    | hairs? | hypan-?thi(a|um)
    | leaf | leaflet | leaves | lobes?
    | petals? | petioles? | petiolules? | pistils? | peduncles?
    | ovar(y|ies) | ovules?
    | racemes?
    | sepals? | stamens? | stigmas? | stipules? | styles?
    )""")

VOCAB.term('leaf', r""" leaf (\s* blades?)? | leaflet | leaves | blades? """)
VOCAB.term('petiole', r""" (?<! to \s ) (petioles? | petiolules?)""")
VOCAB.term('lobes', r' ( leaf \s* )? (un)?lobe[sd]? ')
VOCAB.term('hairs', 'hairs?')
VOCAB.term('flower', fr'({SEX} \s+ )? flowers?')
VOCAB.term('hypanthium', 'hypan-?thi(um|a)')
VOCAB.term('sepal', 'sepals?')
VOCAB.term('calyx', 'calyx | calyces')
VOCAB.term('stamen', 'stamens?')
VOCAB.term('anther', 'anthers?')
VOCAB.term('style', 'styles?')
VOCAB.term('stigma', 'stigmas?')
VOCAB.term('petal', r' petals? ')
VOCAB.term('corolla', r' corollas? ')

VOCAB.term('shape_starter', r"""
    broadly
    | deeply | depressed
    | long
    | mostly
    | narrowly | nearly
    | partly
    | shallowly | sometimes
    """)

VOCAB.part('location', r""" \b ( terminal | lateral | basal | cauline ) """)
VOCAB.term('dim', """
    width wide length long radius diameter diam? """.split())

VOCAB.part('punct', r' [,;:/] ', capture=False, priority=LOWEST)

VOCAB.term('word', r' [a-z] \w* ', capture=False, priority=LOWEST)

# ############################################################################
# Numeric patterns

VOCAB.term('units', ' cm mm '.split())

VOCAB.part('number', r' \d+ ( \. \d* )? ')

# Numeric ranges like: (10–)15–20(–25)
RANGE = r"""
    (?<! slash | dash | number )
    (?: open (?P<min> number ) dash close )?
    (?P<low> number )
    (?: dash (?P<high> number ) )?
    (?: open dash (?P<max> number ) close )?
    (?! dash | slash )
    """
VOCAB.grouper('range', RANGE, capture=False)

# Cross measurements like: 3–5(–8) × 4–11(–13)
# Rename the groups so we can easily extract them in the parsers
RANGE_GROUPS = regex.compile(
    r""" ( min | low | high | max ) """,
    regex.IGNORECASE | regex.VERBOSE)
LENGTH_RANGE = RANGE_GROUPS.sub(r'\1_length', RANGE)
WIDTH_RANGE = RANGE_GROUPS.sub(r'\1_width', RANGE)

CROSS = f"""
    {LENGTH_RANGE} (?P<units_length> units )?
    ( x {WIDTH_RANGE} (?P<units_width> units )? )?
    """
VOCAB.grouper('cross', CROSS, capture=False)

CROSS_GROUPS = regex.compile(
    r""" (length | width) """, regex.IGNORECASE | regex.VERBOSE)
CROSS_1 = CROSS_GROUPS.sub(r'\1_1', CROSS)
CROSS_2 = CROSS_GROUPS.sub(r'\1_2', CROSS)
VOCAB.grouper('sex_cross', f"""
    {CROSS_1} (open)? (?P<sex_1> sex )? (close)?
    ( conj | prep )?
    {CROSS_2} (open)? (?P<sex_2> sex )? (close)?
    """, capture=False)

# Like: "to 10 cm"
VOCAB.grouper(
    'cross_upper',
    fr""" up_to (?P<high_length> number )
        (?P<units_length> units ) """, capture=False)

# Like: "to 10"
VOCAB.grouper(
    'count_upper', fr""" up_to (?P<high> number ) """, capture=False)


def split_keywords(value):
    """Convert a vocabulary string into separate words."""
    return regex.split(fr"""
        \s* \b (?: {VOCAB['conj'].pattern} | {VOCAB['prep'].pattern} )
            \b \s* [,]? \s*
        | \s* [,\[\]] \s*
        """, value, flags=util.FLAGS)


def part_phrase(catalog, leaf_part):
    """Build a grouper rule for the leaf part."""
    return catalog.grouper(f'{leaf_part}_phrase', f"""
            ( location ( word | punct | prep )* )?
            (?P<part> {leaf_part} )
            """)
