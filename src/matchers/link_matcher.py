"""Base matcher object."""

# pylint: disable=import-error
from collections import defaultdict

from traiter.spacy_nlp.matcher import SpacyMatcher

from .attach import ATTACH
from ..pylib.util import LINK_STEP


class LinkMatcher(SpacyMatcher):
    """Base matcher object."""

    name = 'entity_matcher'

    def __init__(self, nlp):
        super().__init__(nlp)
        links = self.add_patterns([ATTACH], LINK_STEP)

        # This is used for sorting matches
        self.priority = {m['label']: m.get('priority', 9999) for m in links}
        for action in self.actions:
            label = action.split('.')[0]
            self.priority[action] = self.priority[label]

    def filter_matches(self, matches):
        """Remove overlapping matches following priority rules."""
        strings = self.nlp.vocab.strings

        # Group matches by priority
        priorities = defaultdict(list)
        for match in matches:
            label = strings[match[0]]
            priority = self.priority[label]
            priorities[priority].append(match)

        # Order matches in each list by longest then leftmost
        for priority, match_list in priorities.items():
            priorities[priority] = sorted(
                match_list, key=lambda m: (m[1] - m[2], m[1]))

        # Build list by adding longest matches w/ no overlap by priority
        match_list = []
        for priority in sorted(priorities.keys()):
            match_list += priorities[priority]

        matches = []
        for curr in match_list:
            for prev in matches:
                if (prev[1] <= curr[1] < prev[2]
                        or prev[1] < curr[2] <= prev[2]
                        or (curr[1] <= prev[1] and curr[2] >= prev[2])):
                    break
            else:
                matches.append(curr)

        return sorted(matches, key=lambda m: m[1])

    @staticmethod
    def closest_part(start, parts):
        """Find the part that is closest to the current match."""
        part = [p for p in parts if p.i < start]
        part = sorted(part, key=lambda p: -p.i)
        return part[0] if part else None

    # pylint: disable=too-many-locals, disable=unused-argument
    def scan(self, doc, matchers, step):
        """Find all terms in the text and return the resulting doc."""
        all_matches = []

        for matcher in matchers:
            all_matches += matcher(doc)

        for sent in doc.sents:
            matches = [m for m in all_matches
                       if m[1] >= sent.start and m[2] <= sent.end]
            matches = self.filter_matches(matches)

            parts = [t for t in sent if t.ent_type_ == 'part']

            for match_id, start, end in matches:
                part = self.closest_part(start, parts)
                span = doc[start:end]
                label = self.nlp.vocab.strings[match_id]
                if action := self.actions.get(label):
                    action(span, part)

        return doc
