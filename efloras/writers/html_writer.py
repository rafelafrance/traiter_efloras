"""Write output to an HTML file."""

import html
from collections import deque, namedtuple
from datetime import datetime
from itertools import cycle

from jinja2 import Environment, FileSystemLoader

from ..matchers.matcher import MATCHERS


# CSS colors
CLASSES = [f'c{i}' for i in range(24)]
COLORS = cycle(CLASSES)

Cut = namedtuple('Cut', 'pos open len id end type title')

TRAIT_SUFFIXES = [m['name'] for m in MATCHERS]


def html_writer(args, rows):
    """Output the data frame."""
    tags = build_tags()

    rows = sorted(rows, key=lambda r: (r['family'], r['taxon']))

    colors = {label for r in rows for label in r['traits']}
    colors -= {'part'}
    colors = {label: next(COLORS) for label in sorted(colors)}

    for row in rows:
        row['text'] = format_text(row, tags, colors)
        row['traits'] = format_traits(row, colors)

    env = Environment(
        loader=FileSystemLoader('./efloras/writers/templates'),
        autoescape=True)

    template = env.get_template('html_writer.html').render(
        now=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),
        rows=rows)
    args.output_file.write(template)
    args.output_file.close()


def format_traits(row, colors):
    """Format the traits for HTML."""
    new_dict = {}
    traits = dict(sorted(row['traits'].items(), key=lambda i: i[0]))
    for label, traits in traits.items():
        if label == 'part':
            continue
        new_label = f'<span class="{colors[label]}">{label}</span>'
        new_traits = {}
        for trait in traits:
            del trait['start']
            del trait['end']
            trait = ', '.join(f'{k}:&nbsp;{v}' for k, v in trait.items())
            new_traits[trait] = 1
        new_dict[new_label] = '<br/>'.join(new_traits.keys())

    return new_dict


def format_text(row, tags=None, colors=None):
    """Colorize and format the text for HTML."""
    text = row['text']
    cuts = []
    cut_id = 0

    for label, traits in row['traits'].items():
        title = ' '.join(label.split('_'))
        for trait in traits:
            if not (color := colors.get(label)):
                continue
            cut_id = append_endpoints(
                cuts, cut_id, trait['start'], trait['end'],
                color, title=title)

    if parts := row['traits'].get('part'):
        for part in parts:
            cut_id = append_endpoints(
                cuts, cut_id, part['start'], part['end'], 'bold')

    return insert_markup(text, cuts, tags)


def insert_markup(text, cuts, tags):
    """Insert formatting markup for text highlighting etc."""
    # Extract function here
    stack = deque()
    parts = []

    prev_end = 0
    for cut in sorted(cuts):

        # Add text before the tag
        if cut.pos != prev_end:
            parts.append(html.escape(text[prev_end:cut.pos]))
            prev_end = cut.pos

        # Add an open tag
        if cut.open:
            tag = tags[(cut.type, True)]
            if cut.title:
                tag = tag.replace('>', f' title="{cut.title}">')
            parts.append(tag)       # Add tag to output
            stack.appendleft(cut)   # Prepend open cut to stack

        # Close tags are more complicated. We have to search for the
        # matching open tag on the stack & remove it. We also need to
        # reopen any intervening open tags. All while adding the
        # appropriate close tags.
        else:
            # Find matching open tag while keeping any intervening tags
            for idx in range(len(stack)):
                # Append closing tag to output
                parts.append(tags[(stack[0].type, False)])

                # Is this the open tag we are looking for?
                # Open tags have a negative ID and close tags are positive.
                # This pushes the tags to the correct position for sorted
                if abs(stack[0].id) == cut.id:
                    break
                stack.rotate(-1)
            else:
                raise IndexError('Matching open tag not found in stack.')
            # Get rid of matching open tag
            stack.popleft()

            # Put intervening open tags back on stack & reopen in text
            for _ in range(idx):
                stack.rotate(1)
                parts.append(tags[(stack[0].type, True)])

    # Handle text after the last closing tag
    if prev_end != len(text):
        parts.append(html.escape(text[prev_end:]))

    return ''.join(parts)


def append_endpoints(cuts, cut_id, start, end, tag_type, title=None):
    """
    Append endpoints to the cuts.

    The only interesting point is that open cuts have a negative len and
    matching close cuts have a positive len. This will push the cuts to the
    correct position during a sort. Longer cuts need to surround inner cuts.

    Like so:
    [open_cut(len=-2), open_cut(len=-1), close_cut(len=1), close_cut(len=2)]

    The same logic applies to the ID field. We push later tags outward:
    [open_cut(id=-2), open_cut(id=-1), close_cut(id=1), close_cut(id=2)]
    """
    cut_id += 1  # Absolute value is the ID
    trait_len = end - start

    cuts.append(Cut(
        pos=start,
        open=True,  # Close tags come before open tags
        len=-trait_len,  # Longest tags open first
        id=-cut_id,  # Force an order. Push open tags leftward
        end=end,
        type=tag_type,
        title=title,
    ))

    cuts.append(Cut(
        pos=end,
        open=False,  # Close tags come before open tags
        len=trait_len,  # Longest tags close last
        id=cut_id,  # Force an order. Push close tags rightward
        end=end,
        type=tag_type,
        title=None,
    ))

    return cut_id


def build_tags():
    """
    Make tags for HTML text color highlighting.

    Tag keys are the the CSS class and if it's an open or close tag.
    For example:
        (css_class, is_open) -> <span class="css_class">
        (css_class, not_open) -> </span>
    """
    tags = {
        ('bold', True): '<strong>',
        ('bold', False): '</strong>',
    }

    for color in CLASSES:
        tags[(color, True)] = f'<span class="{color}">'
        tags[(color, False)] = '</span>'

    return tags
