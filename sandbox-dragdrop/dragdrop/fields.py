from wtforms import Field
from wtforms.utils import unset_value
from wtforms.widgets import NumberInput
from wtforms.widgets import TextInput

class EnumField(Field):
    widget = NumberInput()

    def __init__(self, label=None, validators=None, enumtype=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.enumtype = enumtype

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.enumtype(int(valuelist[0]))

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data is not None:
            return str(self.data.value)
        return ''



