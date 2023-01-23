from plants.writers.html_writer import HtmlWriter as BaseWriter
from tqdm import tqdm

from .. import const
from .html_writer_row import HtmlWriterRow


class HtmlWriter(BaseWriter):
    def __init__(self, out_path):
        super().__init__(
            template_dir=f"{const.ROOT_DIR}/efloras/pylib/writers/templates",
            out_path=out_path,
        )

    def write(self, efloras_rows, in_file_name=""):
        for efloras_row in tqdm(efloras_rows):
            text = self.format_text(efloras_row)
            traits = self.format_traits(efloras_row)
            self.formatted.append(
                HtmlWriterRow(
                    formatted_text=text,
                    formatted_traits=traits,
                    family=efloras_row.family,
                    flora_id=efloras_row.flora_id,
                    taxon=efloras_row.taxon,
                    taxon_id=efloras_row.taxon_id,
                    link=efloras_row.link,
                    path=efloras_row.path,
                )
            )

        self.write_template(in_file_name)
