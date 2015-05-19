from django.db import models
from vlib.vforms import widgets

class VDateField(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.VDateInput}
        defaults.update(kwargs)
        return super(VDateField, self).formfield(**defaults)

class VDateTimeInput(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.VDateInput}
        defaults.update(kwargs)
        return super(VDateField, self).formfield(**defaults)

class VTimeInput(models.DateField):
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.VDateInput}
        defaults.update(kwargs)
        return super(VDateField, self).formfield(**defaults)