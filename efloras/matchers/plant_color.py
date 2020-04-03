"""Common color snippets."""

from spacy.matcher import PhraseMatcher
from .base import Base
from .shared import SHARED_TERMS
from ..pylib.trait import Trait

COLOR_TERMS = {
    'COLOR': """
        black blue brown
        cream cream-yellow creamy crimson
        glaucous-pink gold golden golden-yellow gray gray-green green
        grey grey-green
        ivory ivory-white
        lavendar lavender lemon lilac
        maroon
        olive olive-green orange orange-pink
        pink pink-purple pink-violet purple
        red red-brown rose rose-coloured
        salmon salmon-pink scarlet silver silvery stramineous straw-colored
        sulphur-yellow
        tan
        violet
        white
        yellow
        """.split(),
    'COLOR_LEADER': """
        blackish blueish brownish
        grayish greenish greyish
        pinkish purpleish purplish
        reddish
        violetish
        whitish
        yellowish
        """.split(),
    'COLOR_FOLLOWER': """
        colored
        lined lines longitudinal
        mottled
        spot spots spotted stripe striped stripes
        vein veined veins
        throated tinge tinged tinges tip tipped tips
        """.split(),
    }

RENAME = {
    'blackish': 'black',
    'blueish': 'blue',
    'brownish': 'brown',
    'cream': 'white',
    'cream-yellow': 'yellow',
    'creamy': 'cream',
    'crimson': 'red',
    'glaucous-pink': 'pink',
    'golden-yellow': 'yellow',
    'greyish': 'gray',
    'greenish': 'green',
    'ivory': 'white',
    'lavendar': 'purple',
    'lavender': 'purple',
    'lemon': 'yellow',
    'lilac': 'purple',
    'maroon': 'red-brown',
    'olive-green': 'green',
    'pink-violet': 'pink-purple',
    'pinkish': 'pink',
    'purpleish': 'purple',
    'purplish': 'purple',
    'reddish': 'red',
    'rose': 'pink',
    'rose-coloured': 'pink',
    'salmon-pink': 'orange-pink',
    'scarlet': 'red',
    'silvery': 'silver',
    'stramineous': 'yellow',
    'straw-colored': 'yellow',
    'sulphur-yellow': 'yellow',
    'violet': 'purple',
    'violetish': 'purple',
    'whitish': 'white',
    'yellowish': 'yellow',
    }


class PlantColor(Base):
    """Parse plant colors."""

    def __init__(self):
        super().__init__()
        self.matcher = PhraseMatcher(self.nlp.vocab, attr='LOWER')

        terms = {**SHARED_TERMS, **COLOR_TERMS}
        for label, values in terms.items():
            patterns = [self.nlp.make_doc(x) for x in values]
            self.matcher.add(label, None, *patterns)

    def parse(self, text):
        """Parse the traits."""
        traits = []
        trait = Trait(part='', value='', raw_value='', start=len(text), end=0)
        raw_start, raw_end = len(text), 0
        doc = self.nlp(text)

        matches = self.matcher(doc)
        if not matches:
            return []

        matches = self.first_longest(matches)
        colors = []
        prev_end, prev_label = -99, ''

        for match_id, start, end in matches:
            label = doc.vocab.strings[match_id]
            span = doc[start:end]
            norm = span.text.lower()

            trait.start = min(trait.start, span.start_char)
            trait.end = max(trait.end, span.end_char)
            dist = start - prev_end

            if label == 'PLANT_PART':
                trait.part = norm
            else:
                raw_start = min(raw_start, span.start_char)
                raw_end = max(raw_end, span.end_char)

            if label == 'COLOR':
                color = RENAME.get(norm, norm)
                if (prev_label == ('COLOR_LEADER', 'COLOR')
                        and self.previous_token(dist, doc, start)):
                    colors[-1] += f'-{color}'
                else:
                    colors.append(color)

            elif label == 'COLOR_LEADER':
                color = RENAME.get(norm, norm)
                colors.append(color)

            elif (label == 'COLOR_FOLLOWER'
                    and prev_label in ('COLOR', 'COLOR_FOLLOWER')
                    and self.previous_token(dist, doc, start)):
                colors[-1] += f'-{norm}'

            prev_end, prev_label = end, label

        else:
            trait.raw_value = text[raw_start:raw_end]
            trait.value = sorted(set(colors))
            traits.append(trait)

        return traits


PLANT_COLOR = PlantColor()
