from flask import request
from markupsafe import Markup
from wtforms import Form
from wtforms import RadioField

class CatWidget:
    """
    Render subfields of wtforms.RadioField as siblings with initial tab state.
    """

    def __init__(self, label_class='tab', current_class='current'):
        self.label_class = label_class
        self.current_class = current_class

    def __call__(self, field, **kwargs):
        html = []
        for subfield in field:
            classes = [self.label_class]
            if subfield.checked:
                classes.append(self.current_class)
            class_ = ' '.join(classes)
            html.append(f'{subfield()}{subfield.label(class_=class_)}')
        return Markup(''.join(html))


class PageTabs:
    # NOTES
    # - using radio buttons so the browser handles the checked attribute
    # - value of radio button points to another element's id

    # TODO
    # - a way to zip() or something the tab inputs with matching tab content
    # - just check the index in the template to render the tab?

    def __init__(
        self,
        choices,
        formclass = Form,
        fieldclass = RadioField,
        arg_key = 'tab',
    ):
        self.choices = choices
        self.formclass = formclass
        self.fieldclass = fieldclass
        self.arg_key = arg_key

    @property
    def form(self):
        class TabForm(self.formclass):
            tabs = self.fieldclass(
                choices = self.choices,
                render_kw = dict(
                    # tabs.js
                    class_ = 'tab',
                ),
                widget = CatWidget(),
            )

        form = TabForm()

        if self.arg_key and self.arg_key in request.args:
            form.tabs.data = request.args[self.arg_key]
        else:
            form.tabs.data = self.choices[0][0]

        return form
