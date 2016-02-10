from django import template
from django.conf import settings
#from django.apps import apps as apps_on_project
import os.path
#from vlib import menu_apps
from vlib import menu_apps_templates as menu_apps
from parametro.controle_acesso.views import PermissoesFuncionarios
from django.contrib.auth.models import User

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_menu(context, request):
    """Retorna o html do menu(uma lista)"""
    try:
        emp = context['funcionario']['empresa']
        func = context['funcionario']['id']
    except:
        emp = 0
        func = -1
   
    if func == -1:
        return ""
    
    if context['funcionario']['funcionario_existe']:
        permissoes = PermissoesFuncionarios(id_funcionario=func)
    else:
        permissoes = PermissoesFuncionarios(id_funcionario=-1)
        permissoes.usr = User.objects.get(pk=context['funcionario']['usuario'])
   
    menu = menu_apps.MenuAppsTemplate(permissoes=permissoes)
    return menu.get_apps_html(path=settings.BASE_DIR, empresa=emp)

@register.assignment_tag(takes_context=True)
def get_controle_acesso_apps(context, request):
    """Retorna o html para o controle de acesso menu(uma lista)"""
    try:
        emp = context['funcionario']['empresa']
        func = context['funcionario']['id']
    except:
        emp = 0
        func = -1

    if func == -1:
        return ""
        
    if context['funcionario']['funcionario_existe']:
        permissoes = PermissoesFuncionarios(id_funcionario=func)
    else:
        permissoes = PermissoesFuncionarios(id_funcionario=-1)
        permissoes.usr = User.objects.get(pk=context['funcionario']['usuario'])

    menu = menu_apps.MenuAppsTemplate(permissoes=permissoes)
    return menu.get_apps_html(path=settings.BASE_DIR, empresa=emp, menu=False)
