import json

from markupsafe import Markup

from ..html import Tag
from ..html import render_tag

class Draggable(Tag):
    """
    Render an object as some html that can be dragged.
    """

    def __init__(
        self,
        inner,
        draggable_type = None,
        draggable_data = None,
    ):
        """
        :param inner:
            object to render inside this draggable element, possibly another
            dropzone of draggables.
        :param draggable_type:
            a string type of what type this draggable is.
        :param draggable_data:
            json payload for draggable to carry.
        """
        self.inner = inner
        self.draggable_type = draggable_type
        self.draggable_data = draggable_data

    def draggable_attributes(self):
        return {
            'draggable': 'true',
            'data-draggable-type': self.draggable_type,
            'data-draggable-data': self.draggable_data,
        }

    def __call__(self):
        """
        Render this draggable as an HTML element.
        """
        return render_tag(
            'div',
            Markup(self.inner),
            **self.draggable_attributes(),
        )


class Dropzone(Tag):
    """
    Render an object as some html that can accept types of draggable elements.
    """

    def __init__(
        self,
        *,
        types,
        data = None,
        list_name = None,
        children = None,
        limit = 1,
    ):
        """
        :param list_name:
            name of key for list of nested objects, used by javascript.
        :param types:
            a list of string types this drop zone accepts.
        :param children:
            an iterable of elements this zone contains.
        :param limit:
            integer limit of the number of draggables this zone can contain.
        """
        self.data = data
        self.list_name = list_name
        self.types = types
        if children is None:
            children = []
        self.children = list(children)
        self.limit = limit

    def dropzone_attributes(self):
        data_attributes = dict(
            data_dropzone = True,
            data_list_name = self.list_name,
            data_dropzone_type = self.types,
            data_dropzone_limit = self.limit,
        )
        if self.data is not None:
            data_attributes['data_dropzone_data'] = self.data
        return data_attributes

    def __call__(self):
        return render_tag(
            'div',
            inner = ''.join(map(Markup, self.children)),
            **self.dropzone_attributes(),
        )
