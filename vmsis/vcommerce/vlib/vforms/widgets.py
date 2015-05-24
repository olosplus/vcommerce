from django.forms.widgets import DateTimeBaseInput

class VDateInput(DateTimeBaseInput):
    format_key = 'DATE_INPUT_FORMATS'
    input_type = 'date'

class VDateTimeInput(DateTimeBaseInput):
    format_key = 'DATETIME_INPUT_FORMATS'
    input_type = 'datetime'

class VTimeInput(DateTimeBaseInput):
    format_key = 'TIME_INPUT_FORMATS'
    input_type = 'time'