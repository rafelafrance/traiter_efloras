"""Plant part parser."""


def plant_part(span):
    """Enrich a plant part match."""
    return {'part': span.text.lower()}


PLANT_PART = {
    'name': 'plant_part',
    'trait_names': ['plant_part'],
    'matchers': {
        'plant_part': {
            'on_match': plant_part,
            'patterns': [[{'_': {'term': 'plant_part'}}]],
        },
    }
}
