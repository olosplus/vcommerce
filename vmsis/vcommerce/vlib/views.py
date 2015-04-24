# coding : utf-8
from django.http import HttpResponse
import json
from django.db.models import get_model
from django.apps import apps
from django.core.exceptions import ValidationError
from vlib.filtro import Filtro as FormFiltro
from vlib.grid import Grid
from collections import OrderedDict

#from django.utils.decorators import classonlymethod
LINE_SEPARATOR = "<<LINE_SEPARATOR>>"


#class GridPersistence(object):

#@staticmethod
def insert(data, model, commit = True, link_to_form = "", parent_instance = None):

    if not data:
        return ""
    if link_to_form[-3:].upper() == "_ID":
        link_to_form = link_to_form[:-3]

    if data.count(LINE_SEPARATOR) > 0:
        lista = data.split(LINE_SEPARATOR)    
    else:
        lista = [data]
    
    for row in lista:     
        if not row:
            continue    
        row_json = dict(json.loads(row))
        mod = model()

        for field in model._meta.fields:
            if field.name == 'id':
                continue

            if field.name == link_to_form and commit:
                setattr(mod, field.name, parent_instance)
                continue

            if field.name in row_json:
                setattr(mod, field.name, row_json[field.name])
            else:
                if field.name + '_id' in row_json:
                    setattr(mod, field.name + '_id', row_json[field.name + '_id'])

        try:
            if link_to_form:
                mod.full_clean(exclude = (link_to_form,))
            else:
                mod.full_clean()                    
        except ValidationError as e:            
            return "<input id='grid_erros' value='%s'>" % str(e).replace("'", "").replace('"', "")

        if commit :
            mod.save()        

    return ""    

#@staticmethod    
def delete(data, model):
    lista = data.split(LINE_SEPARATOR)    

    for row in lista:        
        if not row:
            continue
        row_json = dict(json.loads(row))
        mod = model.objects.get(pk=row_json['id'])
        try:
            mod.delete()
        except Error as e:
            return e
        
    return ""    

#@staticmethod
def update(data, model, commit = True):

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

    return ""    

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
        
    fields = json.loads(request.GET.get('columns'), object_pairs_hook=OrderedDict)
    
    fields_display = []
    
    for field in fields:    
        if not field in ["col_update", "col_delete"]:
            fields_display.append(field)
    
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



