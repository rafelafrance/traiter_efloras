"""Common logic for parsing trait notations."""

import spacy
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, \
    CONCAT_QUOTES, HYPHENS, LIST_ELLIPSES, LIST_ICONS


class Base:
    """Shared lexer logic."""

    def __init__(self):
        self.matcher = None

        # TODO make nlp object a singleton

        spacy.prefer_gpu()
        self.nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

        infixes = (
            LIST_ELLIPSES
            + LIST_ICONS
            + [
                r"(?<=[0-9])[+\-\*^](?=[0-9-])",
                r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                    al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES),
                r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
                r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),

                ###############################################
                # Custom interior rules

                # dashes after a number
                r"""(?<=[0-9])(?:{h})(?=[{a}])""".format(h=HYPHENS, a=ALPHA),
                r"""^(?:{h})|(?:{h})$""".format(h=HYPHENS),  # dashes at ends
                r"""[:"=]""",  # for json-like data
                r"(?<=[0-9])\.(?=[{a}])".format(a=ALPHA),   # 1.word, 2.other
                ])
        infix_regex = spacy.util.compile_infix_regex(infixes)
        self.nlp.tokenizer.infix_finditer = infix_regex.finditer

    @staticmethod
    def remove_overlapping(matches):
        """Return the longest of any overlapping matches."""
        if not matches:
            return matches
        first, *rest = sorted(matches, key=lambda m: (m[1], -m[2]))
        return [first] + [m for i, m in enumerate(rest, 1)
                          if m[1] >= matches[i-1][2]]

    def parse(self, text):
        """Parse the traits."""
        raise NotImplementedError
