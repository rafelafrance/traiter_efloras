"""Plant part parser."""


def plant_part(span):
    """Enrich a plant part match."""
    return {'plant_part': span.text.lower()}


PLANT_PART = {
    'plant_part': {
        'on_match': plant_part,
        'patterns': [[{'_': {'term': 'plant_part'}}]],
    },
}
