from dataclasses import dataclass

from plants.writers.base_html_writer_row import BaseHtmlWriterRow


@dataclass(kw_only=True)
class HtmlWriterRow(BaseRow):
    family: str
    flora_id: int
    taxon: str
    taxon_id: int
    link: str
    path: str
