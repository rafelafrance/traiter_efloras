"""Patterns for attaching traits to plant parts."""


def attach(doc):
    """Attach traits to parts."""
    for sent in doc.sents:
        part = ''

        for token in sent:

            if token.ent_type_ == 'part':
                part = token._.data.get('part', '')
            elif part and not token._.data.get('part'):
                token._.data['part'] = part

    return doc
