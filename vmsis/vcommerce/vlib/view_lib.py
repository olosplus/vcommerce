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
from django.db import models
from importlib import import_module
from django.conf import settings
from copy import deepcopy
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


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }

            return JsonResponse(data)
        else:
            return response

class StandardFormGrid(ModelForm):
    child_models = str()
    current_user = None
    grid_erros = str();
    funcionario = None
    nome_campo_empresa = str()
    nome_campo_unidade = str()
    
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
                return e
        
        return str()

    def insert_grid(self, data, model, commit = True, link_to_form = "", parent_instance = None, grid_id = ""):        
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
                re = e.message_dict
                val = []
                for k in list(re.keys()):
                    val.append(k + ":" + \
                    str(re[k]).replace("'", "").replace('"', "").replace("[","").replace("]","" ).replace(",", ".") )
                
                return "<input id='grid_erros' name='%s' value='%s' data-indexrow = '%s'>" % \
                     (grid_id, str(val).replace("'", "").replace('"', "") , row_json['data-indexrow'])
    
            if commit : 
                self.before_insert_grid_row(instance = mod)
                mod.save()                            
                self.after_insert_grid_row(instance = mod)
    
        return str()

    def update_grid(self, data, model, commit = True, grid_id = ""):
    
        if data.count(LINE_SEPARATOR) > 0:
            lista = data.split(LINE_SEPARATOR)    
        else:
            lista = [data]
    
        for row in lista:                
            if not row:
                continue
    
            row_json = dict(json.loads(row))        
            mod = model.objects.get(pk=row_json['id'])
            old_mod = deepcopy(mod)
    
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
                re = e.message_dict
                val = []
                for k in list(re.keys()):
                    val.append(k + ":" + \
                    str(re[k]).replace("'", "").replace('"', "").replace("[","").replace("]","" ).replace(",", ".") )
                
                return "<input id='grid_erros' name='%s' value='%s' data-indexrow = '%s'>" % \
                     (grid_id, str(val).replace("'", "").replace('"', "") , row_json['data-indexrow'])
    
            if commit :                
                self.before_update_grid_row(instance = mod, old_instance = old_mod)
                mod.save()            
                self.after_update_grid_row(instance = mod, old_instance = old_mod)
    
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
                        grid_id = data_dict['grid_id'])                                 
                if erro:
                    return erro
                else:
                    if data_dict['rows_updated']:
                        erro = self.update_grid(data = data_dict['rows_updated'], model = model, commit = False,
                            grid_id = data_dict['grid_id'])
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

    def after_insert_grid_row(self, instance):
        '''override this method to make custom procedures for each grid row inserted.
           This method have a object's instance inserted on the database as parameter(instance)
        '''

    def before_update_grid_row(self, instance, old_instance):
        '''override this method to make custom procedures for each grid row updated.
           This method have a object's instance updated on the database as parameter(instance)
        '''


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
                            link_to_form = data_dict['link_to_form'], parent_instance = parent_instance_pk) 
                    if erro:
                        return erro
    
                    if data_dict['rows_updated']:                        
                        erro = self.update_grid(data = data_dict['rows_updated'], model = model, commit = True)
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
            if self.grid_erros:
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
   
class ViewCreate(CreateView, AjaxableResponseMixin):  
    template_name = TEMPLATE_INSERT
    MediaFiles = []   
    nome_campo_empresa = str()
    nome_campo_unidade = str()

    def set_fields_list(self, request):        
        if not self.fields: 
            self.fields = []
            for field in self.model._meta.fields:
                if field.name.lower() == 'empresa':
                    self.nome_campo_empresa = field.name
                    if request.user.is_superuser:
                        self.fields.append(field.name)
                    continue
                elif field.name.lower() == 'unidade':
                    self.nome_campo_unidade = field.name
                    if request.user.is_superuser:
                        self.fields.append(field.name)
                    continue
                elif field.editable:
                    self.fields.append(field.name)
        
            for field in self.model._meta.many_to_many:
                if field.name.lower() == 'empresa':
                    self.nome_campo_empresa = field.name
                    if request.user.is_superuser:
                        self.fields.append(field.name)
                    continue
                elif field.name.lower() == 'unidade':
                    self.nome_campo_unidade = field.name
                    if request.user.is_superuser:
                        self.fields.append(field.name)
                    continue
                elif field.editable:
                    self.fields.append(field.name)

    def get_success_url(self):
        return self.success_url

    @method_decorator(login_required)  
    def dispatch(self, *args, **kwargs):
        return super(ViewCreate, self).dispatch(*args, **kwargs)

    def __init__(self, **kwargs):
        if 'MediaFiles' in kwargs :
            self.MediaFiles = kwargs.get('MediaFiles')
        if 'nome_campo_empresa' in kwargs :
            self.nome_campo_empresa = kwargs.get('nome_campo_empresa')
        if 'nome_campo_unidade' in kwargs :
            self.nome_campo_unidade = kwargs.get('nome_campo_unidade')

        super(ViewCreate, self).__init__(**kwargs)        

    def get(self, request, *args, **kwargs):
        self.set_fields_list(request)
        return super(ViewCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):        
        self.set_fields_list(request)
        
#        grids_data = request.POST['child_models']
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
                return HttpResponse(error)
            else:
                return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):   
        apps = dict(self.request.session['apps_label'])
        module = self.model.__module__
        module = module.replace(".models", "")
        page_caption = apps[module]

        Urls = urlsCrud(self.model);
        grid = Grid(self.model)
        context = super(ViewCreate, self).get_context_data(**kwargs)   
        context['JsFiles'] = StaticFiles.GetJs(self.MediaFiles)
        context['CssFiles'] = StaticFiles.GetCss(self.MediaFiles)
        context['url_list'] = Urls.BaseUrlList(CountPageBack = 1)
        context['url_insert'] = Urls.BaseUrlInsert(1)
        context['form_id'] = self.model.__name__
        context['grid'] = grid.grid_as_text(use_crud = False, read_only = False, dict_filter = {'id':-1});        
        context['titulo'] = page_caption        
        context['funcionario'] = self.request.session['funcionario']
        return context
 
class ViewUpdate(UpdateView):
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

    def set_fields_list(self, request):
        if not self.fields: 
            self.fields = []
            for field in self.model._meta.fields:
                if field.name.lower() == 'empresa':
                    self.nome_campo_empresa = field.name
                    if request.user.is_superuser:
                        self.fields.append(field.name)
                    continue
                elif field.name.lower() == 'unidade':
                    self.nome_campo_unidade = field.name
                    if request.user.is_superuser:
                        self.fields.append(field.name)
                    continue
                elif field.editable:
                    self.fields.append(field.name)

            for field in self.model._meta.many_to_many:
                if field.name.lower() == 'empresa':
                    self.nome_campo_empresa = field.name
                    if request.user.is_superuser:
                        self.fields.append(field.name)
                    continue
                elif field.name.lower() == 'unidade':
                    self.nome_campo_unidade = field.name
                    if request.user.is_superuser:
                        self.fields.append(field.name)
                    continue
                elif field.editable:
                    self.fields.append(field.name)
    
    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):   
        apps = dict(self.request.session['apps_label'])
        module = self.model.__module__
        module = module.replace(".models", "")
        page_caption = apps[module]

        Urls = urlsCrud(self.model);            
        context = super(UpdateView, self).get_context_data(**kwargs)   
        context['form_id'] = self.model.__name__        
        objeto =  context['object']

        grid = Grid(model = self.model, parent_pk_value = objeto.pk)
        context['grid'] = grid.grid_as_text(use_crud = False, read_only = False);

        context['form_pk'] = objeto.pk
        context['JsFiles'] = StaticFiles.GetJs(self.MediaFiles)
        context['CssFiles'] = StaticFiles.GetCss(self.MediaFiles)    
        context['url_list'] =  Urls.BaseUrlList(CountPageBack = 2)
        context['url_update'] = Urls.BaseUrlUpdate(CountPageBack = 2)        
        context['titulo'] = page_caption                        
        context['funcionario'] = self.request.session['funcionario']        
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ViewUpdate, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.set_fields_list(request)
        return super(ViewUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_fields_list(request)

        grids_data = request.POST.get('child_models', {})

        if self.form_class == None:
            self.form_class = StandardFormGrid

        self.form_class = CreateForm(self.model).create_form(GridsData = grids_data, class_form = self.form_class, \
            user = request.user, colaborador = request.session['funcionario'], \
            campo_empresa = self.nome_campo_empresa, campo_unidade = self.nome_campo_unidade)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.model        
        
        grid_erros = form.get_grids_erros(None)

        if grid_erros:
            return HttpResponse(grid_erros)

        return super(ViewUpdate, self).post(request, *args, **kwargs)         
        
        
class ViewDelete(DeleteView):
    template_name = TEMPLATE_DELETE
    MediaFiles = []

    @method_decorator(login_required)  
    def dispatch(self, *args, **kwargs):
        return super(ViewDelete, self).dispatch(*args, **kwargs)

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

class ViewList(ListView):
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
        page_caption = apps[module]

        context = super(ViewList, self).get_context_data(**kwargs)   
        
        grid = Grid(model = self.model, title = page_caption)
       
        context['JsFiles'] = StaticFiles.GetJs(self.MediaFiles)
        context['CssFiles'] = StaticFiles.GetCss(self.MediaFiles)  
        context['grid'] = grid.grid_as_text(display_fields = self.Grid_Fields, use_crud = True, read_only = True);
        context['titulo'] = page_caption         
        context['funcionario'] = self.request.session['funcionario']        
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ViewList, self).dispatch(*args, **kwargs)

class ConvertView:
    def __init__(self, model):
        self.model = model
        self.Urls = urlsCrud(model);  

    def Update(self, MediaFiles = [],  ClassView = ViewUpdate):

        return ClassView.as_view(model = self.model, success_url = self.Urls.BaseUrlList(CountPageBack=2), 
            template_name = TEMPLATE_UPDATE, MediaFiles = MediaFiles)


    def Create(self, MediaFiles = [], ClassView = ViewCreate):    

        return ClassView.as_view(model = self.model, success_url = self.Urls.BaseUrlList(CountPageBack=2), 
            template_name = TEMPLATE_INSERT, MediaFiles = MediaFiles)    


    def Delete(self, MediaFiles = [], ClassView = ViewDelete):

        return ClassView.as_view(model = self.model, success_url = self.Urls.BaseUrlList(CountPageBack=2), 
            template_name = TEMPLATE_DELETE, MediaFiles = MediaFiles)        

    def List(self, MediaFiles = [], Grid_Fields = [], ClassView = ViewList):

        return ClassView.as_view(model = self.model, template_name = TEMPLATE_LIST, MediaFiles = MediaFiles,
        Grid_Fields = Grid_Fields)

class CrudView:
    def __init__(self, model):
        self.model = model
        self.view = ConvertView(model)
        self.UrlCrud = urlsCrud(model);

    def AsUrl(self, MediaFilesInsert = [], MediaFilesUpdate = [], MediaFilesDelete = [], MediaFilesList = [], 
        GridFields = (), ClassCreate = ViewCreate, ClassUpdate = ViewUpdate, ClassDelete = ViewDelete, 
        ClassList = ViewList):

        urls = patterns('', 
            url(self.UrlCrud.UrlList(), self.view.List(MediaFiles = MediaFilesList, Grid_Fields = GridFields, 
                ClassView = ClassList)),

            url(self.UrlCrud.UrlInsert(), self.view.Create(MediaFiles = MediaFilesInsert, ClassView = ClassCreate)), 

            url(self.UrlCrud.UrlUpdate(), self.view.Update(MediaFiles = MediaFilesUpdate, ClassView = ClassUpdate)),

            url(self.UrlCrud.UrlDelete(), self.view.Delete(MediaFiles = MediaFilesDelete, ClassView = ClassDelete)))

        return urls