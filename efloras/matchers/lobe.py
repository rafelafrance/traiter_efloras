"""Common lobe count snippets."""

# NOTE: We also handle lobes in the attach matcher.


def lobe_count(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
        _relabel='lobe_count',
    )

    for token in span:
        label = token._.label

        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}

        elif label == 'lobe_suffix':
            continue

        else:
            return {}

    return data


def lobe_zero(span):
    """Enrich the match with data."""
    return dict(
        start=span.start_char,
        end=span.end_char,
        low=0,
        _relabel='lobe_count',
    )


LOBE = {
    'name': 'lobe',
    'matchers': [
        {
            'label': 'lobe_count',
            'on_match': lobe_count,
            'patterns': [
                [
                    {'_': {'label': 'range'}},
                    {'_': {'label': 'lobe_suffix'}}
                ],
            ],
        },
        {
            'label': 'lobe_zero',
            'on_match': lobe_zero,
            'patterns': [
                [
                    {'_': {'label': 'lobe_none'}}
                ],
            ],
        },
    ]
}
