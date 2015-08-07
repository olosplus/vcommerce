# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.db import models
import json

from vlib import menu_apps
from cadastro.funcionario.models import Funcionario
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User


class EmptyModel(models.Model):
    pass


# Create your views here.
class PermissoesFuncionarios(object):
    def __init__(self, id_funcionario):        
        funcionario = Funcionario.objects.get(pk = id_funcionario)
        usr = User.objects.get(pk = funcionario.user.id)        
        self.id_funcionario = id_funcionario
        self.usr = usr
    
    def get_permissoes(self, app_label):
        list_permissions = []
        models = apps.get_app_config(app_label).get_models()        

        for model in models:            
            can_add = self.usr.has_perm(app_label + '.add_' + model.__name__.lower())
            can_delete = self.usr.has_perm(app_label + '.delete_' + model.__name__.lower())
            can_change = self.usr.has_perm(app_label + '.change_' + model.__name__.lower())
            list_permissions.append({"verbose_name" : model._meta.verbose_name,
                                     "model" : model.__name__,
                                     "can_add" : can_add,
                                     "can_delete" : can_delete,
                                     "can_change" : can_change})
        return list_permissions
    

    def get_permissoes_json(self, app_label):
        return json.dumps(self.get_permissoes(app_label))
    
    def get_object_permission(self, app_label, model_name, permission_type):
        tela = ContentType.objects.get(app_label = app_label, model = model_name.lower())
        code = permission_type + '_' + model_name.lower()
        return Permission.objects.get(content_type = tela, codename = code)
        
    def add_content_type(self, app_label):
        content = ContentType.objects.filter(app_label = app_label)

        if not content:
            new_content = ContentType(name = "show_" + app_label, app_label = app_label,
                                      model = app_label)
            new_content.save()
            
            new_permission = Permission(content_type = new_content, name = 'Can Show ' + app_label,
                                        codename = 'show_' + app_label)
            new_permission.save()
                
    def liberar_acesso(self, app_label, model_name, permission_type):
        permission = self.get_object_permission(app_label = app_label, model_name = model_name,
                                                permission_type = permission_type)        
        self.usr.user_permissions.add(permission)
    
    def remover_acesso(self, app_label, model_name, permission_type):
        permission = self.get_object_permission(app_label = app_label, model_name = model_name,
                                                permission_type = permission_type)
        self.usr.user_permissions.remove(permission) 
    
    def definir_permissao(self, app_label, model_name, permission_type, liberar):
        if liberar:
            self.liberar_acesso(app_label, model_name, permission_type)
        else:
            self.remover_acesso(app_label, model_name, permission_type)
    
    
    @staticmethod    
    def get_apps_dict():
        return menu_apps.MenuApps.GetAppsVerboseNameAsDict()

    @staticmethod    
    def get_apps_json():
        return json.dumps(PermissoesFuncionarios.get_apps_dict())
    

@login_required
def PaginaPrincipal(request):
    usr_object = Funcionario.objects.all()
    dict_usr = {}
    for usr in usr_object:        
        dict_usr.update({ str(usr.pk) : usr.nome})
    
    dict_usr = json.dumps(dict_usr)
    list_apps = PermissoesFuncionarios.get_apps_json()    
    
    return render_to_response('controle_acesso.html', {"lista_usuarios" : dict_usr, "apps" : list_apps })

def GetPermissoes(request):
    try:
        id_funcionario = request.GET.get('id_funcionario')
        app_module = request.GET.get('module')
        
        list_module = app_module.split('.')
        app_label = list_module[len(list_module) - 1]        
        permissoes = PermissoesFuncionarios(id_funcionario = id_funcionario)
        print(list_module)
        p = permissoes.get_permissoes_json(app_label)        
        if not len(p) == 0:
            permissoes.add_content_type(app_label = app_label)
            p = permissoes.get_permissoes_json(app_label)
        
        return HttpResponse(p)
    
    except Exception as e:
        print(e)
        return HttpResponse(E)
    
def SetPermissoes(request):
    try:
        data = request.GET.get("data")
        list_permissoes_models = json.loads(data)

        for permissoes in list_permissoes_models:
            label = permissoes["app_label"]
            model_name = permissoes["model"]
            can_add = permissoes["can_add"]
            can_change = permissoes["can_change"]
            can_delete = permissoes["can_delete"]
            
            permissoes_func = PermissoesFuncionarios(id_funcionario = permissoes["usuario"])
            
            permissoes_func.definir_permissao(app_label = label, model_name = model_name,
                                              permission_type = 'add', liberar = can_add)

            permissoes_func.definir_permissao(app_label = label, model_name = model_name,
                                              permission_type = 'change', liberar = can_change)
            
            permissoes_func.definir_permissao(app_label = label, model_name = model_name,
                                              permission_type = 'delete', liberar = can_delete)
            
            
        
        return HttpResponse("Dados salvos com sucesso")
    except Exception as e:
        print(e)
        return HttpResponse(E)
