"""Plant part is being  used as a location parser."""

# from traiter.pipes.entity_data import REJECT_MATCH

# PART_LOCATION = [
#     # {
#     #     'label': 'not_a_part_location',
#     #     'on_match': REJECT_MATCH,
#     #     'patterns': [
#     #         [
#     #             {'ENT_TYPE': {'IN': ['sex', 'sex_enclosed', 'location']}},
#     #             {'ENT_TYPE': 'part'},
#     #         ],
#     #     ],
#     # },
#     {
#         'label': 'part_location',
#         'patterns': [
#             [
#                 {'POS': {'IN': ['PART', 'ADP', 'VERB', 'SCONJ']}},
#                 {'ENT_TYPE': 'part'},
#             ],
#         ],
#     },
# ]
