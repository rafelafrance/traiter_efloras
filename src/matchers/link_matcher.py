"""Base matcher object."""

# pylint: disable=import-error
from collections import defaultdict

from traiter.matchers.rule import Rule

from .link import LINK

MATCHERS = [LINK]


class LinkMatcher(Rule):
    """Base matcher object."""

    def __init__(self, nlp, rules, step):
        super().__init__(nlp, rules=rules, step=step)

        # This is used for sorting matches
        self.priority = {r['label']: r.get('priority', 9999) for r in rules}

    def filter_matches(self, matches):
        """Remove overlapping matches following priority rules."""
        strings = self.nlp.vocab.strings

        # Group matches by priority
        priorities = defaultdict(list)
        for match in matches:
            label = strings[match[0]]
            label = label.split('.')[0]
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

    def __call__(self, doc):
        """Find all terms in the text and return the resulting doc."""
        matches = self.matcher(doc)

        for sent in doc.sents:
            matches = [m for m in matches if m[1] >= sent.start and m[2] <= sent.end]
            matches = self.filter_matches(matches)

            parts = [t for t in sent if t.ent_type_ == 'part']

            for match_id, start, end in matches:
                part = self.closest_part(start, parts)
                span = doc[start:end]
                label = self.nlp.vocab.strings[match_id]
                if action := self.actions.get(label):
                    action(span, part)

        return doc
