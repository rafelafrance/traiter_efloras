"""Write training data to a JSONL file."""

import json
from collections import namedtuple


Sents = namedtuple('Sent', 'start end traits')
Trait = namedtuple('Trait', 'start end label')


def training_data_writer(args, rows):
    """Output the data."""

    train_data = []

    for row in rows:
        # Initialize sentences
        sents = [Sents(start=s[0], end=s[1], traits=[]) for s in row['sents']]
        sents = sorted(sents)

        # Initialize traits
        traits = [Trait(start=t['start'], end=t['end'], label=label)
                  for label, ts in row['traits'].items() for t in ts]
        traits = sorted(traits)

        # Attach traits to a sentence
        s = 0
        for trait in traits:
            if trait.start >= sents[s].end:
                s += 1
            sents[s].traits.append(trait)

        # Annotations
        for sent in sents:
            text = row['text'][sent.start:sent.end]
            traits = [(t.start - sent.start, t.end - sent.start, t.label)
                      for t in sent.traits]
            train_data.append([text, {'entities': traits}])

    # Write the data
    json.dump(train_data, args.training_data)
