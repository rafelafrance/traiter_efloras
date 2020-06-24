"""Plant part is being  used as a location parser."""


def part_location(_):
    """Handle a part that is being used as a location."""
    data = {'_relabel': 'part_location'}
    for token in _:
        token._.aux['skip'] = True
    return data


PART_LOCATION = {
    'name': 'part_location',
    'matchers': [
        {
            'label': 'part_location',
            'on_match': part_location,
            'patterns': [[
                {'POS': {'IN': ['PART', 'ADP']}},
                {'_': {'label': 'part'}},
            ]],
        },
    ],
}
