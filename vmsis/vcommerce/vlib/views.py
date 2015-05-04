# coding : utf-8
from django.http import HttpResponse
import json
from django.db.models import get_model
from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError
from vlib.filtro import Filtro as FormFiltro
from vlib.grid import Grid
from vlib.menu_apps import MenuApps
from collections import OrderedDict

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from importlib import import_module
from django.conf import settings
from django.core import serializers

try:
    from cadastro.funcionario.models import Funcionario
    UtilizaFuncionario = True
except ImportError:
    UtilizaFuncionario = False


LINE_SEPARATOR = "<<LINE_SEPARATOR>>"


# Create your views here.

@login_required
def index(request):
     
    request.session['apps_label'] = MenuApps.GetAppsVerboseName()
    
#    if UtilizaFuncionario:
    try:                
        func = Funcionario.objects.get(user = request.user)
        unidades = func.unidade.all()
        list_unidades = []

        for f in unidades:
            list_unidades.append({"id":f.id, "nome":f.nmrazao})    
            
        request.session['funcionario'] = {"id" : func.id, "nome" : func.nome, "usuario" : func.user.id,
            "empresa" : func.empresa.id, "unidades" : list_unidades, "unidade":list_unidades[0]["id"]}
                
    except :
        request.session['funcionario'] = {"id" : request.user.id, "nome" : request.user.username, 
            "usuario" : request.user.id,
            "empresa" : None, "unidades" : None, "unidade":None}

    return render_to_response('base.html', {"funcionario":request.session['funcionario']})

def SetUnidade(request):
    try:
        unidade = request.GET.get('unidade')     
        func = {}
        func.update(request.session['funcionario'])
        if unidade:
            del request.session['funcionario']
            func['unidade'] = unidade
            request.session['funcionario'] = func
        
        return HttpResponse(request.session['funcionario']['unidade'])

    except:
        return HttpResponse('error')

def insert(data, model, commit = True, link_to_form = "", parent_instance = None, 
    execute_on_after_insert = None):

    if not data:
        return str()

    if link_to_form[-3:].upper() == "_ID":
        link_to_form = link_to_form[:-3]

    if data.count(LINE_SEPARATOR) > 0:
        lista = data.split(LINE_SEPARATOR)    
    else:
        lista = [data]
    

    for row in lista:     
        if not row:
            continue    
        
        is_fk_to_parent = False
        model_field_rel_to = None
        link_to_form_alreay_found = False
        exclude_validations = []
        
        row_json = dict(json.loads(row))
        mod = model()
        for field in model._meta.fields:
            is_fk_to_parent = False

            if field.name == 'id':
                continue

            if field.name == link_to_form and not link_to_form_alreay_found:
                if commit:                    
                    setattr(mod, field.name, parent_instance)
                exclude_validations.append(field.name)
                link_to_form_alreay_found = True
                continue
            elif not link_to_form_alreay_found: 
                if field.__class__ == models.ForeignKey:
                    model_field_rel_to = mod._meta.get_field(field.name).rel.to
                    is_fk_to_parent = (model_field_rel_to == parent_instance.__class__ or \
                        model_field_rel_to == parent_instance.__class__.__base__)
    
                if is_fk_to_parent:
                    setattr(mod, field.name, parent_instance)  
                    link_to_form_alreay_found = True
                    exclude_validations.append(field.name)
                    continue 

            if field.name in row_json:
                setattr(mod, field.name, row_json[field.name])
            else:
                if field.name + '_id' in row_json:
                    setattr(mod, field.name + '_id', row_json[field.name + '_id'])

        try:
            mod.full_clean(exclude = tuple(exclude_validations))
        except ValidationError as e:            
            return "<input id='grid_erros' value='%s'>" % str(e).replace("'", "").replace('"', "")

        if commit :            
            mod.save()            
            if execute_on_after_insert :             
                execute_on_after_insert(instance = mod)

    return str()

#@staticmethod    
def delete(data, model, execute_on_before_delete = None):
    lista = data.split(LINE_SEPARATOR)    

    for row in lista:        
        if not row:
            continue
        row_json = dict(json.loads(row))
        mod = model.objects.get(pk=row_json['id'])
        try:
            if execute_on_before_delete:
                execute_on_before_delete(instance = mod)
            mod.delete()
        except Error as e:
            return e
        
    return ""    

#@staticmethod
def update(data, model, commit = True, execute_on_after_update = None):

    if data.count(LINE_SEPARATOR) > 0:
        lista = data.split(LINE_SEPARATOR)    
    else:
        lista = [data]

    for row in lista:                
        if not row:
            continue

        row_json = dict(json.loads(row))        
        mod = model.objects.get(pk=row_json['id'])        

        for field in model._meta.fields:
            if field.name == 'id':
                continue
            if field.name in row_json:
                setattr(mod, field.name, row_json[field.name])
            else:
                if field.name + '_id' in row_json:
                    setattr(mod, field.name + '_id', row_json[field.name + '_id'])

        try:
            mod.full_clean()
        except ValidationError as e:
            return "<input id='grid_erros' value='%s'>" % str(e).replace("'", "").replace('"', "")

        if commit :
            mod.save()
            if execute_on_after_update:
                execute_on_after_update(instance = mod)

    return str()    

#@classonlymethod
def save_grid(request):    
    str_model = request.GET.get('model')
    str_module = request.GET.get('module')
    list_module = str_module.split('.')    

    try:
        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(str_model)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")
    
    data = request.GET.get('rows_inserted')

    if data:
        erro = insert(data, model)
        if erro:
            return HttpResponse(erro)    

    data = request.GET.get('rows_updated')

    if data:
        erro = update(data, model)
        if erro:
            return HttpResponse(erro)
 
    return HttpResponse('Dados atualizados com sucesso!');

#@staticmethod
def get_model_by_string(module, model_name):
    list_module = module.split('.')    

    try:
        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(model_name)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")
    return model

#@staticmethod
def delete_grid(request):    
    str_model = request.GET.get('model')
    str_module = request.GET.get('module')
    list_module = str_module.split('.')    

    try:
        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(str_model)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")

    data = request.GET.get('rows_deleted')

    if data:
        erro = delete(data, model)
        if erro:
            return HttpResponse(erro)
 
    return HttpResponse('Dados atualizados com sucesso!');

def Filtro(request):
   
    str_model = request.GET.get('model')
    str_module = request.GET.get('module')
    
    list_module = str_module.split('.')    

    try:
        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(str_model)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")

    Filtrar = FormFiltro(model = model, request = request)    
    return Filtrar.Response() #HttpResponse(Filtrar.Form_as_p())

def GetGridCrud(request):
    
    str_model = request.GET.get('model')
    str_module = request.GET.get('module')    
    
    page = request.GET.get('page')    
    order_by = request.GET.get('order_by')

    if not order_by:
        order_by = "id"

    if not page:
        page = 1

    list_module = str_module.split('.')    

    partial_search = request.GET.get('partial_search') 

    if request.GET.get('form_serialized'):
        grid_filter = json.loads(request.GET.get('form_serialized'))
    else:
        grid_filter = str()    
        
    OrderedDict_Cols = json.loads(request.GET.get('columns'), object_pairs_hook=OrderedDict)
    
    fields_display = []

    for fields in list(OrderedDict_Cols.items()):

        properties_field = list(fields[1].items())
        if len(properties_field) >= 4: #equal or more than a four properties
            field_to_display = properties_field[len(properties_field)-1][1]
            fields_display.append(field_to_display)
    
    try:
        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(str_model)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")

    dict_filter = {}
    field_name = str()
    
    if grid_filter:
        for field in grid_filter:        
            if field["name"] != "csrfmiddlewaretoken":       

                if field["value"] != "":  
                    
                    try:
                        fk = model._meta.get_field(field["name"]).rel.to
                    except:
                        fk = None
                    
                    if fk :
                        field_name = model._meta.get_field(field["name"]).get_attname_column()[0]                         
                        dict_filter.update({field_name : field["value"]})                        
                    else:
                        field_name = field["name"]
                    
                        if partial_search == "S":
                            dict_filter.update({field_name + "__iexact" : field["value"]})
                        else:    
                            dict_filter.update({field_name + "__icontains": field["value"]})
    
    GridData = Grid(model)            
    
    grid_js = GridData.get_js_grid(use_crud = True, dict_filter = dict_filter,
        display_fields = tuple(fields_display), page = page, order_by = order_by)
    
    return HttpResponse(grid_js)    



