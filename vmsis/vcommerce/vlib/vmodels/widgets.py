from django.db import models
from vlib.vforms import widgets

class VDateField(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.VDateInput}
        defaults.update(kwargs)
        return super(VDateField, self).formfield(**defaults)

class VDateTimeInput(models.DateTimeField):
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.VDateTimeInput}
        defaults.update(kwargs)
        return super(VDateTimeInput, self).formfield(**defaults)

class VTimeInput(models.TimeField):
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.VTimeInput}
        defaults.update(kwargs)
        return super(VTimeInput, self).formfield(**defaults)