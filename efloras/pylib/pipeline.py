from plants.pipeline_builder import PipelineBuilder


def pipeline():
    pipe = PipelineBuilder()
    pipe.add_tokenizer_pipe()
    pipe.add_term_pipe()
    pipe.add_range_pipe()
    pipe.add_parts_pipe()
    pipe.add_simple_traits_pipe()
    pipe.add_numeric_traits_pipe()
    pipe.add_part_locations_pipe()
    pipe.add_taxa_pipe()
    pipe.add_taxon_like_pipe()
    pipe.add_group_traits_pipe()
    pipe.add_delete_partial_traits_pipe()
    pipe.add_merge_pipe()
    pipe.add_link_parts_pipe()
    pipe.add_link_parts_once_pipe()
    pipe.add_link_subparts_pipe()
    pipe.add_link_subparts_suffixes_pipe()
    pipe.add_link_sex_pipe()
    pipe.add_link_location_pipe()
    pipe.add_link_taxa_like_pipe()
    # pipe.add_delete_unlinked_pipe()

    # pipe.add_delete_partial_traits_pipe(name="delete_taxa", partial_traits=["taxon"])

    return pipe
