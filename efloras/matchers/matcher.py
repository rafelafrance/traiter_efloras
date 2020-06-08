"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from .color import COLOR
from .count import COUNT
from .descriptor import DESCRIPTOR, DESCRIPTOR_LABELS
from .habit import HABIT, HABIT_LABELS
from .phrase import PHRASE
from .part import PART
from .shape import SHAPE
from .size import SIZE
from ..pylib.sentencizer import NLP
from ..pylib.terms import TERMS

MATCHERS = (COLOR, COUNT, DESCRIPTOR, HABIT, PHRASE, PART, SHAPE, SIZE)


class Matcher(TraitMatcher):  # pylint: disable=too-few-public-methods
    """Base matcher object."""

    def __init__(self):
        super().__init__(NLP)

        self.plant_wide_labels = set(DESCRIPTOR_LABELS + HABIT_LABELS)

        # Process the matchers
        trait_patterns = []
        group_patterns = {}

        for matcher in MATCHERS:
            trait_patterns += matcher['matchers']
            group_patterns = {**group_patterns, **matcher.get('groupers', {})}

        self.add_trait_patterns(trait_patterns)
        self.add_group_patterns(group_patterns)
        self.add_terms(TERMS)

    def parse(self, text):
        """Parse the traits."""
        doc = super().parse(text)

        traits = defaultdict(list)

        for i, sent in enumerate(doc.sents):
            part = 'plant' if i == 0 else ''
            augment = {}
            suffix_label = {'ok': False, 'label': '', 'data': {}}

            for token in sent:
                label = token._.label
                data = token._.data

                if data.get('relabel'):
                    del data['relabel']

                if label == 'part':
                    part = data['value']

                    # For plant parts we need to consider where the part falls
                    # in a sentence. If it is the first part in a sentence it
                    # is the "base" part and we need to push any fields (like
                    # sex or location) in it to all of the remaining traits &
                    # plant parts in the sentence. For example:
                    #   "Male flowers: petals 4-6 red"
                    # Should be parsed with all traits being "male" like so:
                    #   part: [{'value': 'flower', 'sex': 'male'}
                    #          {'value': 'petal', 'sex': 'male'}]
                    #   petal_count; [{'low': 4, 'high': 6, 'sex': 'male'}]
                    #   petal_color; [{'value': 'red', 'sex': 'male'}]
                    if not augment:
                        augment = {k: v for k, v in data.items()
                                   if k not in ('start', 'end', 'value')}
                    else:
                        data = {**augment, **data}

                    traits['part'].append(data)

                    # Append traits w/ suffix labels like: "2-8(-20) stamens"
                    if suffix_label['ok'] and suffix_label['label']:
                        trait_label = f'{part}_{suffix_label["label"]}'
                        trait_data = {**augment, **suffix_label['data']}
                        traits[trait_label].append(trait_data)
                    if suffix_label['ok']:
                        suffix_label = {'ok': False, 'label': '', 'data': {}}

                # Descriptors and habits can occur anywhere and are not
                # attached to any plant part.
                elif label in self.plant_wide_labels:
                    label = f'plant_{label}'
                    traits[label].append(data)

                elif label == 'suffix_label':
                    suffix_label = {'ok': True, 'label': '', 'data': {}}

                # A trait parse
                elif data and part:
                    # Some traits are written like: with "2-8(-20) stamens"
                    if suffix_label['ok'] and label in ('count', 'color'):
                        suffix_label['label'] = label
                        suffix_label['data'] = {**augment, **data}
                    else:
                        label = f'{part}_{label}'
                        data = {**augment, **data}
                        traits[label].append(data)
                        suffix_label = {'ok': False, 'label': '', 'data': {}}

        # from pprint import pp
        # pp(dict(traits))

        return traits
