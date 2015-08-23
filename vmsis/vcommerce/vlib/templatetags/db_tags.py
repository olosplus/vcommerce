from django import template
from django.core.urlresolvers import resolve
from django.core.handlers.wsgi import WSGIRequest
from vlib import config
from django.apps import apps

register = template.Library()
@register.assignment_tag(takes_context=True)
def get_info_app_name(context, request):   
    return apps.get_app_config('admin').verbose_name

@register.filter(name='get_info')
def get_info(valor, info):
    valor = getattr(config.Config, info)
    return valor

@register.filter(name='get_fk')
def get_fk(fields, key):
    if key in fields:
        return '<a href="javascript:void(0)" class="glyphicon glyphicon-plus inline" \
            onclick="insert(\'%s\', \'%s\', \'%s\', \'%s\')"></a>' % (fields[key]['model'], 
            fields[key]['module'], fields[key]['url'], fields[key]['field_name'])
    else:
        return ''

@register.filter(name='add_class')
def add_class(field, css):
    att = "";
    if 'class' in field.field.widget.attrs:
       att = field.field.widget.attrs['class']
    att += " " + css
    return field.as_widget(attrs={"class":att})
