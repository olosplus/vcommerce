# -*- coding: utf-8 -*-
import json
from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.core import serializers
from vlib.url_lib import urlsCrud
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import models
from django.db import models as modeldb
from django.core.exceptions import ValidationError, ObjectDoesNotExist 
from vlib.grid import Grid
from django.forms import ModelForm, Form
from vlib import views as vlib_views
from django.forms.utils import ErrorList
from django.db import models, transaction
from importlib import import_module
from django.conf import settings
from copy import deepcopy
from django.contrib.auth.decorators import permission_required

#CONSTS
TEMPLATE_INSERT = '_insert_form.html'
TEMPLATE_UPDATE = '_update_form.html'
TEMPLATE_DELETE = '_delete_form.html'
TEMPLATE_LIST = '_list_form.html'
GRID_SEPARATOR = "[[<<ROW_SEPARATOR>>]]"
DOT_CSS = '.CSS'
DOT_JAVA_SCRIPT = '.JS'
LINE_SEPARATOR = "<<LINE_SEPARATOR>>"


class StaticFiles:  
    @staticmethod
    def GetSameTypeFiles(ListOfFiles, Extension):
        files = []       
        for media in ListOfFiles:
            if media[media.index('.'):].upper() == Extension.upper():
                files.append(media)    
        return tuple(files)

    @staticmethod
    def GetCss(ListOfFiles):
        return StaticFiles.GetSameTypeFiles(ListOfFiles = ListOfFiles, Extension = DOT_CSS)

    @staticmethod
    def GetJs(ListOfFiles):
        return StaticFiles.GetSameTypeFiles(ListOfFiles = ListOfFiles, Extension = DOT_JAVA_SCRIPT)


class StandardFormGrid(ModelForm):
    child_models = str()
    current_user = None
    grid_erros = str()
    funcionario = None
    nome_campo_empresa = str()
    nome_campo_unidade = str()
    grids_child_map = {}
    
    @staticmethod
    def formatMsgError(model_name, msg, index =-1):
        return "<input id='grid_erros' name='%s' value='%s' data-indexrow = '%s'>" % \
                (model_name, str(msg).replace("'", "").replace('"', "") , index)
    
    def delete_grid(self, data, model):
        
        lista = data.split(LINE_SEPARATOR)
    
        for row in lista:        
            if not row:
                continue
            row_json = dict(json.loads(row))
            mod = model.objects.get(pk=row_json['id'])
            try:
                self.before_delete_grid_row(instance = mod)                    
                mod.delete()                
            except Exception as e:                
                print(e)
                return e
        
        return str()

    def insert_grid(self, data, model, commit = True, link_to_form = "", parent_instance = None, grid_id = "", \
        parent_model = ""):        
        if not data:
            return str()
        
        if link_to_form[-3:].upper() == "_ID":
            link_to_form = link_to_form[:-3]
    
        if data.count(LINE_SEPARATOR) > 0:
            lista = data.split(LINE_SEPARATOR)    
        else:
            lista = [data]
        
        maps = {}
        erro = str()
        for row in lista:     
            if not row:
                continue    
            
            is_fk_to_parent = False
            model_field_rel_to = None
            link_to_form_already_found = False
            exclude_validations = []

            row_json = dict(json.loads(row))
            
            mod = model()
            for field in model._meta.fields:
                is_fk_to_parent = False

                if field.name == 'id':
                    continue
                
                if field.name.lower() == 'empresa':
                    setattr(mod, field.get_attname_column()[0], self.funcionario['empresa'])
                    continue

                if field.name.lower() == 'unidade':
                    setattr(mod, field.get_attname_column()[0], self.funcionario['unidade'])
                    continue

                if field.name == link_to_form and not link_to_form_already_found:
                    if commit:                    
                        if parent_model in self.grids_child_map:
                            if row_json['data-parent-indexrow'] in self.grids_child_map[parent_model]:
                                setattr(mod, field.get_attname_column()[0], self.grids_child_map[parent_model]\
                                    [row_json['data-parent-indexrow']])
                            else:
                                setattr(mod, field.name, parent_instance)
                        else:
                            setattr(mod, field.name, parent_instance)
                    
                    exclude_validations.append(field.name)
                    link_to_form_already_found = True
                    continue
                elif not link_to_form_already_found: 
                    if field.__class__ == models.ForeignKey:
                        model_field_rel_to = mod._meta.get_field(field.name).rel.to
                        is_fk_to_parent = (model_field_rel_to == parent_instance.__class__ or \
                            model_field_rel_to == parent_instance.__class__.__base__)
        
                    if is_fk_to_parent:
                        setattr(mod, field.name, parent_instance)  
                        link_to_form_already_found = True
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
                re = e.message_dict
                val = []
                for k in list(re.keys()):
                    val.append(k + ":" + \
                    str(re[k]).replace("'", "").replace('"', "").replace("[","").replace("]","" ).replace(",", ".") )
                
                return "<input id='grid_erros' name='%s' value='%s' data-indexrow = '%s'>" % \
                     (grid_id, str(val).replace("'", "").replace('"', "") , row_json['data-indexrow'])
            
            if commit : 
                erro = self.before_insert_grid_row(instance = mod)                
                if erro:
                    return self.formatMsgError(mod.__class__.__name__, erro)
                mod.save()

                maps.update({row_json['data-indexrow'] : mod.id})

                erro = self.after_insert_grid_row(instance = mod)

                if erro:
                    return self.formatMsgError(mod.__class__.__name__, erro)


        if commit:
            self.grids_child_map.update({mod.__class__.__name__ : maps})
        
        return str()

    def update_grid(self, data, model, commit = True, grid_id = "", parent_model = ""):
    
        if data.count(LINE_SEPARATOR) > 0:
            lista = data.split(LINE_SEPARATOR)    
        else:
            lista = [data]
        maps = {}
        erro = str()
        for row in lista:                
            if not row:
                continue
    
            row_json = dict(json.loads(row))        
            mod = model.objects.get(pk=row_json['id'])
            old_mod = deepcopy(mod)
    
            for field in model._meta.fields:
                if field.name == 'id':
                    continue
                
                if field.name.lower() == 'empresa':                    
                    setattr(mod, field.get_attname_column()[0], self.funcionario['empresa'])
                    continue

                if field.name.lower() == 'unidade':
                    setattr(mod, field.get_attname_column()[0], self.funcionario['unidade'])
                    continue

                if field.name in row_json:
                    setattr(mod, field.name, row_json[field.name])
                else:
                    if field.name + '_id' in row_json:
                        setattr(mod, field.name + '_id', row_json[field.name + '_id'])
    
            try:
                mod.full_clean()
            except ValidationError as e:
                re = e.message_dict
                val = []
                for k in list(re.keys()):
                    val.append(k + ":" + \
                    str(re[k]).replace("'", "").replace('"', "").replace("[","").replace("]","" ).replace(",", ".") )
                
                return "<input id='grid_erros' name='%s' value='%s' data-indexrow = '%s'>" % \
                     (grid_id, str(val).replace("'", "").replace('"', "") , row_json['data-indexrow'])
    
            if commit :                
                erro = self.before_update_grid_row(instance = mod, old_instance = old_mod)
                
                if erro:
                    return self.formatMsgError(mod.__class__.__name__, erro)

                mod.save()            
                maps.update({row_json['data-indexrow'] : mod.id})
                
                erro = self.after_update_grid_row(instance = mod, old_instance = old_mod)

                if erro:
                    return self.formatMsgError(mod.__class__.__name__, erro)

        if commit:
            self.grids_child_map.update({mod.__class__.__name__ : maps})
            
        return str()    

    def split_child_models(self):        
        return self.child_models.split(GRID_SEPARATOR)
                     
    def get_grids_erros(self, parent_instance):        
        
        erro = ""
        if self.child_models:
            grids = self.split_child_models()           

            for grid in grids:
                if not grid:
                    continue                
                data_dict = json.loads(grid)                

                if not 'rows_inserted' in data_dict:
                    continue
                
                model = vlib_views.get_model_by_string(data_dict['module'], data_dict['model'])
                
                if data_dict['rows_inserted']:
                    erro = self.insert_grid(data = data_dict['rows_inserted'], model = model, commit = False,
                        link_to_form = data_dict['link_to_form'], parent_instance = parent_instance, 
                        grid_id = data_dict['grid_id'], parent_model = data_dict['parent'])
                print('pass54')           
                print(erro)
                if erro:
                    return erro
                else:
                    if data_dict['rows_updated']:
                        erro = self.update_grid(data = data_dict['rows_updated'], model = model, commit = False,
                            grid_id = data_dict['grid_id'], parent_model = data_dict['parent'])
                    if erro:                        
                        return erro

        return str()

    def custom_grid_validations(self, grid_model, grid_data, parent_instance):
        '''override this method to make custom validations'''
        return str()

    def before_insert_grid_row(self, instance):
        '''override this method to make custom procedures for each grid row inserted.
           This method have a object's instance inserted on the database as parameter(instance)
        '''
        return str()

    def after_insert_grid_row(self, instance):
        '''override this method to make custom procedures for each grid row inserted.
           This method have a object's instance inserted on the database as parameter(instance)
        '''
        return str()

    def before_update_grid_row(self, instance, old_instance):
        '''override this method to make custom procedures for each grid row updated.
           This method have a object's instance updated on the database as parameter(instance)
        '''
        return str()


    def after_update_grid_row(self, instance, old_instance):
        '''override this method to make custom procedures for each grid row updated.
           This method have a object's instance updated on the database as parameter(instance)
        '''

    def before_delete_grid_row(self, instance):
        '''override this method to make custom procedures for each grid row that will be delete.
           This method have a object's instance that will be deleted on the database as parameter(instance)
        '''


    def save_grids(self, parent_instance_pk):        
        erro = str()

        if self.child_models:            
            
            grids = self.split_child_models()
            
            for grid in grids:
                
                if not grid:
                    continue                    
          
                data_dict = json.loads(grid)        
                model = vlib_views.get_model_by_string(data_dict['module'], data_dict['model'])
                
                erro = self.custom_grid_validations(grid_model = model, grid_data = data_dict, \
                    parent_instance = parent_instance_pk)
                
                if erro:
                    return erro
                
                if 'rows_deleted' in data_dict:                                                        
                    if data_dict['rows_deleted']:
                        return self.delete_grid(data = data_dict['rows_deleted'], model = model)                                  
                else:
                    if data_dict['rows_inserted']:                    
                        
                        erro = self.insert_grid(data = data_dict['rows_inserted'], model = model, commit = True,
                            link_to_form = data_dict['link_to_form'], parent_instance = parent_instance_pk,
                            parent_model = data_dict['parent']) 
                        
                    if erro:
                        return erro
    
                    if data_dict['rows_updated']:                        
                        erro = self.update_grid(data = data_dict['rows_updated'], model = model, commit = True,
                            parent_model = data_dict['parent'])
                        if erro:
                            return erro
        return str()        

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
            initial=None, error_class=ErrorList, label_suffix=None,
            empty_permitted=False, instance=None):

        if data:            
            copy_data = data.copy()

            if self.funcionario:        
                try:
                    if self.nome_campo_empresa:
                        if self.funcionario['empresa']:
                            copy_data[self.nome_campo_empresa] = self.funcionario['empresa']
                except :
                    pass

                try:
                    if self.nome_campo_unidade:
                        if self.funcionario['unidade']:
                            copy_data[self.nome_campo_unidade] = self.funcionario['unidade']
                except :
                    pass
        else:
            copy_data = None    

        super(StandardFormGrid, self).__init__(data=copy_data, files=files, auto_id=auto_id, prefix=prefix,
            initial= initial, error_class=error_class, label_suffix=label_suffix,
            empty_permitted=empty_permitted, instance=instance)

    def get_instace(self):
        return super(StandardFormGrid, self).save(commit=False)

    def save(self, commit = True):

        instance = super(StandardFormGrid, self).save(commit = commit)
        
        if commit:              
            self.grid_erros = self.save_grids(parent_instance_pk = instance)
            self.erros = self.grid_erros

            if self.grid_erros:
                self.erros = self.grid_erros
                return None

        return instance    

class CreateForm(object):
    def __init__(self, model):
        self.model = model

    def create_form(self, class_form = StandardFormGrid, GridsData = "", user = None, colaborador = None,
        campo_empresa = str(), campo_unidade = str()):
        class vmsisForm(class_form):                    
            class Meta:
                model = self.model                
            
            child_models = GridsData
            current_user = user
            funcionario = colaborador
            nome_campo_unidade = campo_unidade
            nome_campo_empresa = campo_empresa

        return vmsisForm

class StandardCrudView(object):
    
    fks_fields = {}
    show_fields = []

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):        
        has_permission = True
        
        if not self.request.session["funcionario"] :
            return HttpResponse(msg_permission_html)
        else:
            usr =  self.request.user
        
        operation = ''
        
        if issubclass(self.__class__, CreateView):
            operation = '.add_'
        elif issubclass(self.__class__, UpdateView):
            operation = '.change_'
        elif issubclass(self.__class__, DeleteView):
            operation = '.delete_'
        
        if operation:
            has_permission = usr.has_perm(self.model._meta.app_label + operation +
                                          self.model.__name__.lower())
        
        if has_permission:    
            return super(StandardCrudView, self).dispatch(*args, **kwargs)
        else:            
            return render_to_response('access_danied.html');
    
    def set_fields_list(self):        
        rel_to = None
        self.fks_fields = {}
        self.show_fields = []
        
        for field in self.model._meta.fields:                
            try:
                rel_to = field.rel.to
            except Exception as e:
                rel_to = None
                
            if not rel_to is None:
                to_include_in_fk = True

                if hasattr(self.model._meta, 'exclude_fk_plus'):                
                    if(field.name in self.model._meta.exclude_fk_plus):
                        to_include_in_fk = False

                if to_include_in_fk:
                    url = urlsCrud(rel_to)
                    self.fks_fields.update({ field.name:{'module': rel_to.__module__, 
                        'model': rel_to.__name__, 'url':url.BaseUrlInsert(CountPageBack=2), 'field_name':field.name} })
            
            if field.name.lower() == 'empresa':
                self.nome_campo_empresa = field.name
                if self.request.user.is_superuser:
                    self.show_fields.append(field.name)
                continue
            elif field.name.lower() == 'unidade':
                self.nome_campo_unidade = field.name
                if self.request.user.is_superuser:
                    self.show_fields.append(field.name)
                continue
            elif field.editable:
                self.show_fields.append(field.name)
    
        for field in self.model._meta.many_to_many:
            if field.name.lower() == 'empresa':
                self.nome_campo_empresa = field.name
                if self.request.user.is_superuser:
                    self.show_fields.append(field.name)
                continue
            elif field.name.lower() == 'unidade':
                self.nome_campo_unidade = field.name
                if self.request.user.is_superuser:
                    self.show_fields.append(field.name)
                continue
            elif field.editable:
                self.show_fields.append(field.name)
        self.fields = self.show_fields
   
class ViewCreate(StandardCrudView, CreateView):  
    template_name = TEMPLATE_INSERT
    MediaFiles = []   
    nome_campo_empresa = str()
    nome_campo_unidade = str()

    def get_success_url(self):
        URL = urlsCrud(self.model)
        try:
           id = self.object.id
           return URL.BaseUrlUpdate(CountPageBack = 1) + str(id)
        except Exception as e:
            print(e)
            return self.success_url
                
    def __init__(self, **kwargs):
        if 'MediaFiles' in kwargs :
            self.MediaFiles = kwargs.get('MediaFiles')
        if 'nome_campo_empresa' in kwargs :
            self.nome_campo_empresa = kwargs.get('nome_campo_empresa')
        if 'nome_campo_unidade' in kwargs :
            self.nome_campo_unidade = kwargs.get('nome_campo_unidade')        

        super(ViewCreate, self).__init__(**kwargs)        

    def get(self, request, *args, **kwargs):
        self.set_fields_list()
        return super(ViewCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):        
        self.set_fields_list()
        grids_data = request.POST.get('child_models', {})

        if self.form_class == None:
            self.form_class = StandardFormGrid
        
        self.form_class = CreateForm(self.model).create_form(GridsData = grids_data, class_form = self.form_class, \
            user = request.user, colaborador = request.session['funcionario'], \
            campo_empresa = self.nome_campo_empresa, campo_unidade = self.nome_campo_unidade)
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.model
        
        if form.is_valid():
            
            instance = form.get_instace()            
            
            error = form.get_grids_erros(instance)
            
            if error:
                transaction.rollback()
                return HttpResponse(error)
            else:
                f = self.form_valid(form)
                if form.grid_erros:
                    transaction.rollback()
                    return HttpResponse(form.grid_erros)
                else:
                    return f
        else:
            return self.form_invalid(form)

    def get_grid_instance(self):
        return Grid(self.model)

    def get_context_data(self, **kwargs):   
        apps = dict(self.request.session['apps_label'])
        module = self.model.__module__
        module = module.replace(".models", "")
        try:
            page_caption = apps[module]
        except Exception:
            page_caption = ''

        Urls = urlsCrud(self.model);
        grid = self.get_grid_instance()
        
        self.set_fields_list()
        
        context = super(ViewCreate, self).get_context_data(**kwargs)   

        context['JsFiles'] = StaticFiles.GetJs(self.MediaFiles)
        context['CssFiles'] = StaticFiles.GetCss(self.MediaFiles)
        context['url_list'] = Urls.BaseUrlList(CountPageBack = 1)
        context['url_insert'] = Urls.BaseUrlInsert(1)
        context['form_id'] = self.model.__name__
        context['grid'] = grid.grid_as_text(use_crud = False, read_only = False, dict_filter = {'id':-1},
            exclude_fields = ('empresa', 'unidade'));
        context['titulo'] = page_caption        
        context['funcionario'] = self.request.session['funcionario']
        context['fks'] = self.fks_fields
        context['show_fields'] = self.show_fields
        return context
 
class ViewUpdate(StandardCrudView, UpdateView):
    template_name = TEMPLATE_UPDATE
    MediaFiles = []
    nome_campo_empresa = str()
    nome_campo_unidade = str()

    def __init__(self, **kwargs):
        if 'MediaFiles' in kwargs :
            self.MediaFiles = kwargs.get('MediaFiles')
        if 'nome_campo_empresa' in kwargs :
            self.nome_campo_empresa = kwargs.get('nome_campo_empresa')
        if 'nome_campo_unidade' in kwargs :
            self.nome_campo_unidade = kwargs.get('nome_campo_unidade')

        super(ViewUpdate, self).__init__(**kwargs)
    
    def get_success_url(self):
        return self.success_url

    def get_grid_instance(self, parent_pk_value):
        return Grid(model = self.model, parent_pk_value = parent_pk_value)

    def get_context_data(self, **kwargs):   
        apps = dict(self.request.session['apps_label'])
        module = self.model.__module__
        module = module.replace(".models", "")
        try:
            page_caption = apps[module]
        except Exception:
            page_caption = ''


        Urls = urlsCrud(self.model);            
        
        self.set_fields_list()

        context = super(UpdateView, self).get_context_data(**kwargs)   
        context['form_id'] = self.model.__name__        
        objeto =  context['object']

        grid = self.get_grid_instance(parent_pk_value = objeto.pk)
        
        context['grid'] = grid.grid_as_text(use_crud = False, read_only = False,
            exclude_fields = ('empresa', 'unidade'));

        context['form_pk'] = objeto.pk
        context['JsFiles'] = StaticFiles.GetJs(self.MediaFiles)
        context['CssFiles'] = StaticFiles.GetCss(self.MediaFiles)    
        context['url_list'] =  Urls.BaseUrlList(CountPageBack = 2)
        context['url_update'] = Urls.BaseUrlUpdate(CountPageBack = 2)
        context['url_insert'] = Urls.BaseUrlInsert(CountPageBack = 2)
        context['titulo'] = page_caption                        
        context['funcionario'] = self.request.session['funcionario']        
        context['fks'] = self.fks_fields
        context['show_fields'] = self.show_fields
        return context

    def get(self, request, *args, **kwargs):
        self.set_fields_list()
        return super(ViewUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_fields_list()

        grids_data = request.POST.get('child_models', {})

        if self.form_class == None:
            self.form_class = StandardFormGrid

        self.form_class = CreateForm(self.model).create_form(GridsData = grids_data, class_form = self.form_class, \
            user = request.user, colaborador = request.session['funcionario'], \
            campo_empresa = self.nome_campo_empresa, campo_unidade = self.nome_campo_unidade)
        
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if form.is_valid():
           
            instance = form.get_instace()            
            
            error = form.get_grids_erros(instance)
            
            if error:
                transaction.rollback()
                return HttpResponse(error)
            else:
                f = self.form_valid(form)
                if form.grid_erros:
                    transaction.rollback()
                    return HttpResponse(form.grid_erros)
                else:
                    return f
        else:
            return self.form_invalid(form)

                
class ViewDelete(StandardCrudView, DeleteView):
    template_name = TEMPLATE_DELETE
    MediaFiles = []

    def __init__(self, **kwargs):
        if 'MediaFiles' in kwargs :
            self.MediaFiles = kwargs.get('MediaFiles')
        super(ViewDelete, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):   
        Urls = urlsCrud(self.model);
        context = super(ViewDelete, self).get_context_data(**kwargs)   
        context['JsFiles'] = StaticFiles.GetJs(self.MediaFiles)
        context['CssFiles'] = StaticFiles.GetCss(self.MediaFiles)    
        context['url_list'] = Urls.BaseUrlList(CountPageBack = 1)
        context['funcionario'] = self.request.session['funcionario']        
        return context

class ViewList(StandardCrudView, ListView):
    template_name = TEMPLATE_LIST
    MediaFiles = []
    Grid_Fields =()
    def __init__(self, **kwargs):
        if 'MediaFiles' in kwargs :
            self.MediaFiles = kwargs.get('MediaFiles')
        if 'Grid_Field' in kwargs :
            self.Grid_Fields = kwargs.get('Grid_Fields')
        super(ViewList, self).__init__(**kwargs)

    
    def get_context_data(self, **kwargs):   
        apps = dict(self.request.session['apps_label'])
        module = self.model.__module__
        module = module.replace(".models", "")
        try:
            page_caption = apps[module]
        except Exception:
            page_caption = ''

        context = super(ViewList, self).get_context_data(**kwargs)   
        
        grid = Grid(model = self.model, title = page_caption)
       
        context['JsFiles'] = StaticFiles.GetJs(self.MediaFiles)
        context['CssFiles'] = StaticFiles.GetCss(self.MediaFiles)  
        context['grid'] = grid.grid_as_text(display_fields = self.Grid_Fields, use_crud = True, read_only = True);
        context['titulo'] = page_caption         
        context['funcionario'] = self.request.session['funcionario']        
        return context

class ConvertView:
    def __init__(self, model):
        self.model = model
        self.Urls = urlsCrud(model);  

    def Update(self, MediaFiles = [],  ClassView = ViewUpdate, TemplateName = TEMPLATE_UPDATE):

        return ClassView.as_view(model = self.model, success_url = self.Urls.BaseUrlList(CountPageBack=2), 
            template_name = TemplateName, MediaFiles = MediaFiles)


    def Create(self, MediaFiles = [], ClassView = ViewCreate, TemplateName = TEMPLATE_INSERT):    

        return ClassView.as_view(model = self.model, success_url = self.Urls.BaseUrlList(CountPageBack=2), 
            template_name = TemplateName, MediaFiles = MediaFiles)    


    def Delete(self, MediaFiles = [], ClassView = ViewDelete, TemplateName = TEMPLATE_DELETE):

        return ClassView.as_view(model = self.model, success_url = self.Urls.BaseUrlList(CountPageBack=2), 
            template_name = TemplateName, MediaFiles = MediaFiles)        

    def List(self, MediaFiles = [], Grid_Fields = [], ClassView = ViewList, TemplateName = TEMPLATE_LIST):

        return ClassView.as_view(model = self.model, template_name = TemplateName, MediaFiles = MediaFiles,
            Grid_Fields = Grid_Fields)

class CrudView:
    def __init__(self, model):
        self.model = model
        self.view = ConvertView(model)
        self.UrlCrud = urlsCrud(model);

    def AsUrl(self, MediaFilesInsert = [], MediaFilesUpdate = [], MediaFilesDelete = [], MediaFilesList = [], 
        GridFields = (), ClassCreate = ViewCreate, ClassUpdate = ViewUpdate, ClassDelete = ViewDelete, 
        ClassList = ViewList, TemplateInsert = TEMPLATE_INSERT, TemplateUpdate = TEMPLATE_UPDATE,
        TemplateDelete = TEMPLATE_DELETE, TemplateList = TEMPLATE_LIST):

        urls = patterns('', 
            url(self.UrlCrud.UrlList(), self.view.List(MediaFiles = MediaFilesList, Grid_Fields = GridFields, 
                ClassView = ClassList, TemplateName = TemplateList)),

            url(self.UrlCrud.UrlInsert(), self.view.Create(MediaFiles = MediaFilesInsert, ClassView = ClassCreate,
                TemplateName = TemplateInsert)), 

            url(self.UrlCrud.UrlUpdate(), self.view.Update(MediaFiles = MediaFilesUpdate, ClassView = ClassUpdate,
                TemplateName = TemplateUpdate)),

            url(self.UrlCrud.UrlDelete(), self.view.Delete(MediaFiles = MediaFilesDelete, ClassView = ClassDelete,
                TemplateName = TemplateDelete)))

        return urls