import html
import itertools

from plants.writers import html_writer as phtml
from plants.writers import writer_utils as wutils
from tqdm import tqdm

from .. import consts

SKIPS = {"start", "end", "trait", "part", "subpart"}


def write(args, rows):
    css_classes = phtml.CssClasses()
    formatted = []

    for row in tqdm(rows):
        text = format_text(row, css_classes)
        traits = format_traits(row, css_classes)
        formatted.append(phtml.Formatted(text, traits))

    phtml.write_template(args, consts.ROOT_DIR, "efloras", formatted)


def format_text(row, css_classes):
    """Wrap traits in the text with spans that can be formatted with CSS."""
    frags = []
    prev = 0

    for trait in row.traits:
        start = trait["start"]
        end = trait["end"]

        if prev < start:
            frags.append(html.escape(row.text[prev:start]))

        label = wutils.get_label(trait)
        cls = css_classes[label]

        title = ", ".join(
            f"{k}:&nbsp;{v}" for k, v in trait.items() if k not in wutils.TITLE_SKIPS
        )

        frags.append(f'<span class="{cls}" title="{title}">')
        frags.append(html.escape(row.text[start:end]))
        frags.append("</span>")
        prev = end

    if len(row.text) > prev:
        frags.append(html.escape(row.text[prev:]))

    text = "".join(frags)
    return text


def format_traits(row, css_classes):
    traits = []

    sortable = []
    for trait in row.traits:
        label = wutils.get_label(trait)
        title = row.text[trait["start"] : trait["end"]]
        if trait["trait"] not in wutils.DO_NOT_SHOW:
            sortable.append(phtml.SortableTrait(label, trait["start"], trait, title))

    sortable = sorted(sortable)

    for label, grouped in itertools.groupby(sortable, key=lambda x: x.label):
        cls = css_classes[label]
        label = f'<span class="{cls}">{label}</span>'
        trait_list = []
        for trait in grouped:
            fields = ", ".join(
                f'<span title="{trait.title}">{k}:&nbsp;{v}</span>'
                for k, v in trait.trait.items()
                if k not in wutils.TRAIT_SKIPS
            )
            if fields:
                trait_list.append(fields)

        if trait_list:
            traits.append(phtml.Trait(label, "<br/>".join(trait_list)))

    return traits
