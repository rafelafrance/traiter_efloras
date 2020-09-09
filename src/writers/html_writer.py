"""Write output to an HTML file."""

from collections import defaultdict
from datetime import datetime
from html import escape
from itertools import cycle

from jinja2 import Environment, FileSystemLoader

COLOR_COUNT = 14
BACKGROUNDS = cycle([f'c{i}' for i in range(COLOR_COUNT)])
BORDERS = cycle([f'b{i}' for i in range(COLOR_COUNT)])


def html_writer(args, rows):
    """Output the data."""
    rows = sorted(rows, key=lambda r: (r['flora_id'], r['family'], r['taxon']))

    classes = build_classes(rows)

    for row in rows:
        row['raw_text'] = row['text']
        row['text'] = format_text(row, classes)
        row['traits'] = format_traits(row, classes)

    env = Environment(
        loader=FileSystemLoader('./src/writers/templates'),
        autoescape=True)

    template = env.get_template('html_writer.html').render(
        now=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),
        rows=rows)
    args.html_file.write(template)
    args.html_file.close()


def build_classes(rows):
    """Make tags for HTML text color highlighting.

    Tag keys are the trait name and if it's an open or close tag.
    For example:
        (trait_name, is_open) -> <span class="css_class">
        (trait_name, not_open) -> </span>
    """
    backgrounds = {}
    borders = {}

    tags = {
        'part': 'bold',
        'subpart': 'bold-italic',
    }

    for row in rows:
        for trait in row['traits']:
            name = trait['trait']
            if name in {'part', 'subpart'}:
                continue
            name_parts = name.split('_')
            bg, border = name_parts[0], name_parts[-1]
            if bg not in backgrounds:
                backgrounds[bg] = next(BACKGROUNDS)
            if border not in borders:
                borders[border] = next(BORDERS)
            classes = f'{backgrounds[bg]} {borders[border]} c{backgrounds[bg]}'
            tags[name] = classes
    return tags


def format_traits(row, classes):
    """Format the traits for HTML."""
    new_dict = {}

    # Group by trait name
    groups = defaultdict(list)
    for trait in row['traits']:
        if trait['trait'] not in {'part', 'subpart'}:
            groups[trait['trait']].append(trait)
    groups = dict(sorted(groups.items(), key=lambda i: i[0]))

    # Format each trait group
    for name, traits in groups.items():
        span = f'<span class="{classes[name]}">{name}</span>'

        # Format each trait within a trait group
        new_traits = []
        for trait in traits:
            text = row['raw_text'][trait['start']:trait['end']]
            trait = ', '.join(f'<span title="{text}">{k}:&nbsp;{v}</span>'
                              for k, v in trait.items()
                              if k not in ('start', 'end', 'trait'))
            new_traits.append(trait)
        new_dict[span] = '<br/>'.join(new_traits)

    return new_dict


def format_text(row, classes):
    """Colorize and format the text for HTML."""
    text = row['raw_text']
    frags = []

    prev = 0
    for trait in row['traits']:
        name = trait['trait']
        label = ' '.join(trait['trait'].split('_'))
        start = trait['start']
        end = trait['end']
        title = ', '.join(f'{k} = {v}' for k, v in trait.items()
                          if k not in {'start', 'end', 'trait'})
        title = f'{label}: {title}'
        if prev < start:
            frags.append(escape(text[prev:start]))
        frags.append(f'<span class="{classes[name]}" title="{title}">')
        frags.append(escape(text[start:end]))
        frags.append('</span>')
        prev = end

    if len(text) > prev:
        frags.append(text[prev:])

    return ''.join(frags)
