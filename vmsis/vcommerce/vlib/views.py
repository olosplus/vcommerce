# coding : utf-8
from django.http import HttpResponse
import json
from django.db.models import get_model
from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError
from vlib.dynamic_forms import Dynamic as FormFiltro
from vlib.grid import Grid
from vlib.menu_apps import MenuApps
from collections import OrderedDict

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from importlib import import_module
from django.conf import settings
from django.core import serializers
from vlib.vReport.vReport import PageHeader, MasterBand, PageFooter, Report

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
    
    try:                
        func = Funcionario.objects.get(user = request.user)
        unidades = func.unidade.all()
        list_unidades = []

        for f in unidades:
            list_unidades.append({"id":f.id, "nome":f.nmrazao})    
        
        empresa_id = ""
        
        if func.empresa:
            empresa_id = func.empresa.id

        request.session['funcionario'] = {"id" : func.id, "nome" : func.nome, "usuario" : func.user.id,
            "empresa" : empresa_id, "unidades" : list_unidades, "unidade":list_unidades[0]["id"],
            "is_superuser": request.user.is_superuser}
                
    except :
        request.session['funcionario'] = {"id" : request.user.id, "nome" : request.user.username, 
            "usuario" : request.user.id,
            "empresa" : None, "unidades" : None, "unidade":None, "is_superuser": request.user.is_superuser}

    return render_to_response('base.html', {"funcionario":request.session['funcionario']})

@login_required
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
#@login_required
#def insert(data, model, commit = True, link_to_form = "", parent_instance = None, 
#    execute_on_after_insert = None, grid_id = ""):
#
#    if not data:
#        return str()
#
#    if link_to_form[-3:].upper() == "_ID":
#        link_to_form = link_to_form[:-3]
#
#    if data.count(LINE_SEPARATOR) > 0:
#        lista = data.split(LINE_SEPARATOR)    
#    else:
#        lista = [data]
#    
#
#    for row in lista:     
#        if not row:
#            continue    
#        
#        is_fk_to_parent = False
#        model_field_rel_to = None
#        link_to_form_alreay_found = False
#        exclude_validations = []
#        
#        row_json = dict(json.loads(row))
#        mod = model()
#        for field in model._meta.fields:
#            is_fk_to_parent = False
#
#            if field.name == 'id':
#                continue
#
#            if field.name == link_to_form and not link_to_form_alreay_found:
#                if commit:                    
#                    setattr(mod, field.name, parent_instance)
#                exclude_validations.append(field.name)
#                link_to_form_alreay_found = True
#                continue
#            elif not link_to_form_alreay_found: 
#                if field.__class__ == models.ForeignKey:
#                    model_field_rel_to = mod._meta.get_field(field.name).rel.to
#                    is_fk_to_parent = (model_field_rel_to == parent_instance.__class__ or \
#                        model_field_rel_to == parent_instance.__class__.__base__)
#    
#                if is_fk_to_parent:
#                    setattr(mod, field.name, parent_instance)  
#                    link_to_form_alreay_found = True
#                    exclude_validations.append(field.name)
#                    continue 
#
#            if field.name in row_json:
#                setattr(mod, field.name, row_json[field.name])
#            else:
#                if field.name + '_id' in row_json:
#                    setattr(mod, field.name + '_id', row_json[field.name + '_id'])
#
#        try:
#            mod.full_clean(exclude = tuple(exclude_validations))
#        except ValidationError as e:                      
#            re = e.message_dict
#            val = []
#            for k in list(re.keys()):
#                val.append(k + ":" + \
#                str(re[k]).replace("'", "").replace('"', "").replace("[","").replace("]","" ).replace(",", ".") )
#            
#            return "<input id='grid_erros' name='%s' value='%s' data-indexrow = '%s'>" % \
#                 (grid_id, str(val).replace("'", "").replace('"', "") , row_json['data-indexrow'])
#
#        if commit :            
#            mod.save()            
#            if execute_on_after_insert :             
#                execute_on_after_insert(instance = mod)
#
#    return str()
#
#@login_required
#def delete(data, model, execute_on_before_delete = None):
#    lista = data.split(LINE_SEPARATOR)    
#
#    for row in lista:        
#        if not row:
#            continue
#        row_json = dict(json.loads(row))
#        mod = model.objects.get(pk=row_json['id'])
#        try:
#            if execute_on_before_delete:
#                execute_on_before_delete(instance = mod)
#            mod.delete()
#        except Error as e:
#            return e
#        
#    return ""    
#
#@login_required
#def update(data, model, commit = True, execute_on_after_update = None, grid_id = ""):
#
#    if data.count(LINE_SEPARATOR) > 0:
#        lista = data.split(LINE_SEPARATOR)    
#    else:
#        lista = [data]
#
#    for row in lista:                
#        if not row:
#            continue
#
#        row_json = dict(json.loads(row))        
#        mod = model.objects.get(pk=row_json['id'])        
#
#        for field in model._meta.fields:
#            if field.name == 'id':
#                continue
#            if field.name in row_json:
#                setattr(mod, field.name, row_json[field.name])
#            else:
#                if field.name + '_id' in row_json:
#                    setattr(mod, field.name + '_id', row_json[field.name + '_id'])
#
#        try:
#            mod.full_clean()
#        except ValidationError as e:
#            re = e.message_dict
#            val = []
#            for k in list(re.keys()):
#                val.append(k + ":" + \
#                str(re[k]).replace("'", "").replace('"', "").replace("[","").replace("]","" ).replace(",", ".") )
#            
#            return "<input id='grid_erros' name='%s' value='%s' data-indexrow = '%s'>" % \
#                 (grid_id, str(val).replace("'", "").replace('"', "") , row_json['data-indexrow'])
#
#        if commit :
#            mod.save()
#            if execute_on_after_update:
#                execute_on_after_update(instance = mod)
#
#    return str()    
#
#@login_required
#def save_grid(request):    
#    str_model = request.GET.get('model')
#    str_module = request.GET.get('module')
#    list_module = str_module.split('.')    
#
#    try:
#        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(str_model)
#    except LookupError:
#        return HttpResponse("An error ocurred. The model or module don't exists")
#    
#    data = request.GET.get('rows_inserted')
#
#    if data:
#        erro = insert(data, model)
#        if erro:
#            return HttpResponse(erro)    
#
#    data = request.GET.get('rows_updated')
#
#    if data:
#        erro = update(data, model)
#        if erro:
#            return HttpResponse(erro)
# 
#    return HttpResponse('Dados atualizados com sucesso!');
#
#
def get_model_by_string(module, model_name):
    list_module = module.split('.')    

    try:
        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(model_name)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")
    return model

#@login_required
#def delete_grid(request):    
#    str_model = request.GET.get('model')
#    str_module = request.GET.get('module')
#    list_module = str_module.split('.')    
#
#    try:
#        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(str_model)
#    except LookupError:
#        return HttpResponse("An error ocurred. The model or module don't exists")
#
#    data = request.GET.get('rows_deleted')
#
#    if data:
#        erro = delete(data, model)
#        if erro:
#            return HttpResponse(erro)
# 
#    return HttpResponse('Dados atualizados com sucesso!');

@login_required
def Filtro(request):
   
    str_model = request.GET.get('model')
    str_module = request.GET.get('module')
    
    list_module = str_module.split('.')    

    try:
        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(str_model)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")

    Filtrar = FormFiltro(model = model, request = request, template="filtro.html")    
    return Filtrar.Response()

@login_required
def GetGridConfiguration(request):
    str_model = request.GET.get('model')
    str_module = request.GET.get('module')    
    str_parent = request.GET.get('parent_model')    
    str_parent_module = request.GET.get('parent_module')
    parent_id = request.GET.get('parent_id')
    
    parent_model = None
    if(str_parent_module and str_parent):
        parent_model = get_model_by_string(str_parent_module, str_parent)
    
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
            if field_to_display:
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
    
    return {"model" : model, "filter" : dict_filter, "fields" : fields_display, "page" : page, "order" : order_by,
       "parent":parent_model, "parent_id":parent_id}

@login_required
def GetGridCrud(request):
    try:
        conf = GetGridConfiguration(request = request)    
    
        GridData = Grid(conf["model"])            
        
        grid_js = GridData.get_js_grid(use_crud = True, dict_filter = conf["filter"],
            display_fields = tuple(conf["fields"]), page = conf["page"], order_by = conf["order"])
    except Exception as e:
        print(e)
    return HttpResponse(grid_js)  

@login_required
def PrintGrid(request):
    
    try:
       conf = GetGridConfiguration(request = request)               
    except Exception as e:
        print(e)
    
    model = conf["model"]
    fields = conf["fields"]    
    columns_size = 765 / (len(fields));

    try:
        
        header = PageHeader()
        
        style_label_header = 'font-family: "Times New Roman", Times, serif; font-style: normal;font-size: 20px; '\
            'font-weight: bold;margin:13px auto 3px;max-width:100px';
    
        header.set_style(style = "border-bottom:solid 1px black" )    
        
        header.add_component(type = "p", name = "lblTitulo", text = request.GET.get("title"), 
            style = style_label_header)    
        
        header.add_component(type = "p", name = "lblLinhaHeader", text = "", 
            style = "border-bottom:solid 1px black;")    
        
        for field in fields:
            if field.upper() == "ID" or field.strip() == '':                
                continue
            
            
            if field.find('__') >= 0:
                field = field[0:field.find('__')]

            header.add_component(type="p", name=field, text= model._meta.get_field(field).verbose_name , 
                style="margin:3px 5px 3px 1px; float:left;width:%spx; font-weight:bold" % columns_size)
        
        footer = PageFooter()
        footer.set_style(style = "border-top:solid 1px black" )    

        footer.add_component(type = "p", name = "lblTitulo", text = "vmsis", 
            style = style_label_header)    
    
        master = MasterBand()    
        
        for field in fields:            
            if field.upper() == "ID" or field.strip() == '':
                continue

            master.add_component(type = "dataP", name=field, db_link=field, 
                style="margin:3px 5px 3px 1px;float:left;width:%spx" %columns_size)

    except Exception as e:
        return HttpResponse(e)
        print(e)

    try:        
        
        if conf["filter"]:
            q = model.objects.filter(**conf["filter"])
        else:
            q = model.objects.all()
        
#        if conf["order"]:
#            q = q.order_by(conf["order"])
        
        q = q.values(*fields)        
        master.query = q
        
        report = Report(page_header = header, master_band = master, page_footer = footer,
            template="", page_title = request.GET.get("title"))
        return HttpResponse(report.get_rel_configuration() ) #get_rel_configuration()
    except Exception as e:
        print(e)
        return HttpResponse(e)

@login_required
def GetDataLookup(request):
    str_model = request.GET.get('model')
    str_module = request.GET.get('module')
    
    list_module = str_module.split('.')    

    try:
        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(str_model)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")
    
    query = model.objects.all()
    str_objects = []
    id_values = []
    data = []

    for q in query:
        data.append({"object":str(q), "value":str(q.id)})
    
    return HttpResponse(str(data))

