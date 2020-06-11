"""Common lobe count snippets."""

from ..pylib.terms import REPLACE


def suffixed_count(span):
    """Enrich the match with data."""
    data = dict(
        start=span.start_char,
        end=span.end_char,
    )

    for token in span:
        label = token._.label

        if label == 'range' and token._.data['_all_ints']:
            data = {**token._.data, **data}

        elif label == 'suffix_count':
            relabel = f'{REPLACE[token.lower_]}_count'
            data['_relabel'] = relabel

        else:
            return {}

    return data


def count_zero(span):
    """Enrich the match with data."""
    return dict(
        start=span.start_char,
        end=span.end_char,
        low=0,
        _relabel=f'{REPLACE[span.lower_]}_count',
    )


SUFFIX_COUNT = {
    'name': 'lobe',
    'matchers': [
        {
            'label': 'suffixed_count',
            'on_match': suffixed_count,
            'patterns': [
                [
                    {'_': {'label': 'range'}},
                    {'_': {'label': 'suffix_count'}}
                ],
            ],
        },
        {
            'label': 'count_zero',
            'on_match': count_zero,
            'patterns': [
                [
                    {'_': {'label': 'count_none'}}
                ],
            ],
        },
    ]
}
