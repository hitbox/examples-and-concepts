import json
import unittest

from abc import ABCMeta
from abc import ABC
from abc import abstractmethod

from itertools import groupby
from itertools import starmap
from operator import attrgetter

from markupsafe import Markup

# objects to keep complicated html rendering out of the templates

class Tag(ABC):

    @abstractmethod
    def __call__(self):
        ...

    def __html__(self):
        return self()

    def __str__(self):
        return self()


class Card(Tag):
    """
    <article>
        <header>...</header>
        <div>...</div>
    </article>
    """

    def __init__(
        self,
        header = None,
        body = None,
        collapse_body = True,
    ):
        self.header = header
        self.body = body
        self.collapse_body = collapse_body

    def __call__(self):
        html_list = [
            '<article class="card">',
        ]
        html_list.append('<header>')
        if self.header:
            html_list.append(self.header)
        html_list.append('</header>')

        need_tag = (
            not self.collapse_body
            and not already_tag(self.body, 'div')
        )
        if need_tag:
            html_list.append('<div>')
        if self.body:
            html_list.append(self.body)
        if need_tag:
            html_list.append('</div>')

        html_list.append('</article>')
        return Markup(''.join(map(Markup, html_list)))


class List(Tag):

    def __init__(self, html_list, container_tag='div', sep='', **attributes):
        self.html_list = list(html_list)
        self.container_tag = container_tag
        self.sep = sep
        self.attributes = attributes

    def __call__(self, **extra_attributes):
        inner = self.sep.join(map(Markup, self.html_list))
        return Markup(
            render_tag(
                self.container_tag,
                inner = inner,
                **self.attributes,
            )
        )


def already_tag(obj, tag_name):
    tag_value = getattr(obj, 'tag_name', None)
    return tag_value == tag_name

def clean_key(key):
    if key == 'class_':
        key = 'class'
    return key.replace('_', '-')

def attribute_string(key, value):
    key = clean_key(key)
    if not isinstance(value, str):
        value = json.dumps(value)
    return f"""{key}='{value}'"""

def render_tag(tag_name, inner=None, **attributes):
    # build the parts of the opening tag
    tag_parts = [tag_name]
    pairs = ((key, value) for key, value in attributes.items() if value is not None)
    tag_parts += list(starmap(attribute_string, pairs))
    html = f'<{" ".join(tag_parts)}>'
    if inner:
        html += str(inner)
    html += f'</{tag_name}>'
    return html
