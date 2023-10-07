from markupsafe import Markup

class EmptyWidget:
    """
    Render nothing widget.
    """

    def __call__(self, field, **kwargs):
        return Markup('')


class SubfieldsWidget:
    """
    Render subfields without a container element.
    """

    def __call__(self, field, **kwargs):
        html = [subfield() for subfield in field]
        return Markup(''.join(html))
