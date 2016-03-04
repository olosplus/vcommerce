# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import json

from vlib import menu_apps, menu_apps_templates
from cadastro.funcionario.models import Funcionario
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User


# Create your views here.
class PermissoesFuncionarios(object):
    def __init__(self, id_funcionario):
        try:
            funcionario = Funcionario.objects.get(pk = id_funcionario)
            usr = User.objects.get(pk = funcionario.user.id)
        except Exception as e:
            usr = None
        self.id_funcionario = id_funcionario
        self.usr = usr
        
    
    def get_permissoes(self, app_label):
        list_permissions = []
        models = apps.get_app_config(app_label).get_models()
        is_superuser = self.usr.is_superuser;
        show_whithout_model = True
        
        for model in models:
            show_whithout_model = False
            can_add = self.usr.has_perm(app_label + '.add_' + model.__name__.lower()) or is_superuser
            can_delete = self.usr.has_perm(app_label + '.delete_' + model.__name__.lower()) or is_superuser
            can_change = self.usr.has_perm(app_label + '.change_' + model.__name__.lower()) or is_superuser
            can_show = self.usr.has_perm(app_label + '.show_' + model.__name__.lower()) or is_superuser
            list_permissions.append({"verbose_name" : model._meta.verbose_name,
                                     "model" : model.__name__,
                                     "can_add" : can_add,
                                     "can_delete" : can_delete,
                                     "can_change" : can_change,
                                     "can_show" : can_show})
        else:
            if show_whithout_model:            
                can_show = self.usr.has_perm(app_label + '.show_' + app_label) or is_superuser            
                list_permissions.append({"verbose_name" : app_label,
                                      "model" : app_label,
                                      "can_show" : can_show})
            
        return list_permissions
    
    def get_permissao(self, app_label, permission_type, model_name=""):

        permissoes = self.get_permissoes(app_label=app_label)
        if not permissoes:
            return False
        
        if model_name:
            for permissao in permissoes:
                if permissao["model"] == model_name:
                    if 'can_' + permission_type in permissao:
                        return permissao['can_' + permission_type]                    
        else:            
            if 'can_' + permission_type in permissoes[0]:                
                return permissoes[0]['can_'+permission_type]
        
            
    def get_permissoes_json(self, app_label):
        return json.dumps(self.get_permissoes(app_label))
    
    
    
    def get_object_permission(self, app_label, model_name, permission_type):
        try:
            tela = ContentType.objects.get(app_label = app_label, model = model_name.lower())
        except:
            self.add_content_type(app_label, model_name)
            tela = ContentType.objects.get(app_label = app_label, model = model_name.lower())
            
        code = permission_type + '_' + model_name.lower()
        try:
           return Permission.objects.get(content_type = tela, codename = code)
        except ObjectDoesNotExist as e:
            self.add_content_type(app_label=app_label, model_name=model_name)
            return Permission.objects.get(content_type = tela, codename = code)
        
        
            
    def add_content_type(self, app_label, model_name):
        content = ContentType.objects.filter(app_label = app_label)

        if not content:
            new_content = ContentType(name = "show_" + app_label, app_label = app_label,
                                      model = app_label)
            new_content.save()
            self.add_content_type_permission(model_name = model_name, content_type = new_content)
        else:
            self.add_content_type_permission(model_name = model_name, content_type = content.first())
    
    def add_content_type_permission(self, model_name, content_type):
        
        per = Permission.objects.filter(codename = 'show_' + model_name.lower(),  content_type = content_type)
        if not per:
            new_permission = Permission(content_type = content_type, name = 'Can Show ' + model_name,
                                        codename = 'show_' + model_name.lower())
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
    
    
    def get_apps_html(self):        
        menu = menu_apps_templates.MenuAppsTemplate(self)
        return menu.get_apps_html(path=settings.BASE_DIR, menu=False, hab_UL=True)        

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
    if request.session['funcionario']['funcionario_existe']:    
       list_apps = PermissoesFuncionarios(request.session['funcionario']['id']).get_apps_html()
    else:
        permissoes = PermissoesFuncionarios(id_funcionario=-1)
        permissoes.usr = request.user        
        list_apps = permissoes.get_apps_html()
    
    return render_to_response('controle_acesso.html', {"lista_usuarios" : dict_usr, "apps" : list_apps, "request" : request })

def GetPermissoes(request):
    try:
        id_funcionario = request.GET.get('id_funcionario')
        app_module = request.GET.get('module')
        
        list_module = app_module.split('.')
        app_label = list_module[len(list_module) - 1]        
        permissoes = PermissoesFuncionarios(id_funcionario = id_funcionario)
        p = permissoes.get_permissoes_json(app_label)        

        if not len(p) == 0:
            models = apps.get_app_config(app_label).get_models()            
            for model in models:                        
                permissoes.add_content_type(model_name=model.__name__, app_label = app_label)
        
        p = permissoes.get_permissoes_json(app_label)
        
        
        return HttpResponse(p)
    
    except Exception as e:
        print(e)
        return HttpResponse(e)
    
def SetPermissoes(request):
    try:
        data = request.GET.get("data")
        list_permissoes_models = json.loads(data)

        for permissoes in list_permissoes_models:
            permissoes_func = PermissoesFuncionarios(id_funcionario = permissoes["usuario"])
            
            if 'app_label' in permissoes:
                label = permissoes["app_label"]

            if 'model' in permissoes:
                models = [permissoes["model"]]
            else:
                models = [m.__name__ for m in apps.get_app_config(label).get_models()]
            
            for model_name in models: 
                if 'can_add' in permissoes:
                    can_add = permissoes["can_add"]
                    permissoes_func.definir_permissao(app_label = label, model_name = model_name,
                        permission_type = 'add', liberar = can_add)
                
                if 'can_change' in permissoes:
                    can_change = permissoes["can_change"]
                    permissoes_func.definir_permissao(app_label = label, model_name = model_name,
                        permission_type = 'change', liberar = can_change)
                
                if 'can_delete' in permissoes:
                    can_delete = permissoes["can_delete"]
                    permissoes_func.definir_permissao(app_label = label, model_name = model_name,
                        permission_type = 'delete', liberar = can_delete)
                    
                if 'can_show' in permissoes:
                    can_show = permissoes["can_show"]                
                    permissoes_func.definir_permissao(app_label = label, model_name = model_name,
                        permission_type = 'show', liberar = can_show)
            else:               
                if 'can_show' in permissoes:
                    can_show = permissoes["can_show"]                
                    permissoes_func.definir_permissao(app_label = label, model_name = label,
                        permission_type = 'show', liberar = can_show)

        return HttpResponse("Dados salvos com sucesso")
    except Exception as e:
        print(e)
        return HttpResponse("Dados não salvos. Houver um erro ao definir os acessos.")
