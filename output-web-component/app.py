from flask import Flask
from flask import render_template
from wtforms import Field
from wtforms import FieldList
from wtforms import Form
from wtforms import FormField
from wtforms import IntegerField
from wtforms.widgets import html_params

app = Flask(__name__)

class OutputWidget:

    def __init__(self, tag_name='output'):
        self.tag_name = tag_name

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('is', 'custom-output')
        kwargs.setdefault('data-func', 'areaOfSquare')

        # FIXME
        # - need the dynamically generated name/id of the bound field.
        # - passing field from the class declaration does not work.
        if field.for_fields:
            ids = [other.name for other in field.for_fields]
            kwargs.setdefault('for', ' '.join(ids))

        tag = f'<{self.tag_name}'
        if kwargs:
            tag += ' '
            tag += html_params(**kwargs)
        tag += '>'

        html = [
            # FIXME
            '<script>'
            'function areaOfSquare(elements) {'
            '    return Number(elements[0].value) * Number(elements[1].value);'
            '}'
            '</script>',
            tag,
        ]
        if field.data is not None:
            html.append(str(field.data))
        html.append(f'</{self.tag_name}')
        return ''.join(html)


class OutputField(Field):

    widget = OutputWidget()

    def __init__(
        self,
        label = None,
        validators = None,
        for_fields = None,
        **kwargs,
    ):
        """
        <output> field or similar.
        """
        super().__init__(label , validators, **kwargs)
        if for_fields is None:
            for_fields = []
        self.for_fields = for_fields

    def finalize_for_ids(self):
        """
        Run after form creation to gather the final ids of the referenced
        fields.
        """
        # TODO
        # - I don't see any other way to get these except as a separate
        #   function after form creation.
        # - maybe a form mixin to do this
        # - can we put something on the meta object to do this?


class RectForm(Form):
    width = IntegerField()
    height = IntegerField()
    area = OutputField(
        for_fields = [
            # TODO
            # - pass unbound field objects
            # - handle dynamic field ids
            width,
            height,
        ],
    )


class DemoForm(Form):
    squares = FieldList(FormField(RectForm))


def make_rect(width, height):
    return dict(width=width, height=height, area=width*height)

@app.route('/')
def index():
    """
    Demo a web component automatically calculate and display a value from
    inputs.
    """
    form = DemoForm(
        data = dict(
            squares = [
                make_rect(10, 12),
                make_rect(5, 8),
                make_rect(2, 2),
                make_rect(115, 150),
                make_rect(10, 12),
                make_rect(10, 12),
            ],
        ),
    )
    context = dict(
        form = form,
    )
    return render_template('demo.html', **context)
