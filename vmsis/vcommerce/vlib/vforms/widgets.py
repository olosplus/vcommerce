from django.forms.widgets import DateTimeBaseInput
from django.utils import formats

class VDateTimeBaseInput(DateTimeBaseInput):
    format_key = ''
    supports_microseconds = False

    def __init__(self, attrs=None, format=None):
        super(DateTimeBaseInput, self).__init__(attrs)
        self.format = format if format else None

    def _format_value(self, value):
        return formats.localize_input(value,
            self.format or formats.get_format(self.format_key)[2])

class VDateInput(VDateTimeBaseInput):
    format_key = 'DATE_INPUT_FORMATS'
    input_type = 'date'

class VDateTimeInput(VDateTimeBaseInput):
    format_key = 'DATETIME_INPUT_FORMATS'
    input_type = 'datetime'

class VTimeInput(VDateTimeBaseInput):
    format_key = 'TIME_INPUT_FORMATS'
    input_type = 'time'