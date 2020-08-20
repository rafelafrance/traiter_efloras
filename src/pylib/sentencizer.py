"""Custom sentence splitter."""

import re


ABBREVS = '|'.join("""
    Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec """.split())
ABBREVS = re.compile(fr'(?: {ABBREVS} ) $', flags=re.VERBOSE)


def custom_sentencizer(doc):
    """Break the text into sentences."""
    for i, token in enumerate(doc[:-1]):
        next_token = doc[i + 1]
        if (token.text == '.' and re.match(r'[A-Z]', next_token.prefix_)
                and not ABBREVS.match(next_token.text)):
            next_token.is_sent_start = True
        else:
            next_token.is_sent_start = False

    return doc
