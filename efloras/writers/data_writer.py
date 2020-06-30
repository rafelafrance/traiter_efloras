"""Write training data to a JSONL file."""

import json

from traiter.util import DotDict  # pylint: disable=import-error


def ner_writer(args, rows):
    """Output the data."""
    for row in rows:
        # Initialize sentences
        sents = [DotDict(start=s[0], end=s[1], traits=[])
                 for s in row['sents']]
        sents = sorted(sents, key=lambda s: (s.start, s.end))

        # Initialize traits
        traits = [DotDict(start=t['start'], end=t['end'], label=label)
                  for label, ts in row['traits'].items() for t in ts]
        traits = sorted(traits, key=lambda t: (t.start, t.end, t.label))

        # Attach traits to a sentence
        for sent in sents:
            sent.traits = [t for t in traits
                           if t.start >= sent.start and t.end <= sent.end]

        # Write the data
        for sent in sents:
            text = row['text'][sent.start:sent.end]
            traits = [(t.start - sent.start, t.end - sent.start, t.label)
                      for t in sent.traits]
            line = json.dumps([text, {'entities': traits}])
            args.data_file.write(line)
            args.data_file.write('\n')
