from wtforms import Form
from wtforms import HiddenField
from wtforms import SubmitField
from wtforms.validators import DataRequired

class DragDropForm(Form):
    """
    Simple form for javascript to put nested data into a json field and submit
    through the normal html machinery.
    """
    dragdrop_json = HiddenField(validators=[DataRequired()])
    save = SubmitField()
