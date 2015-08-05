# -*- coding: utf-8 -*-
from vlib.view_lib import CrudView
from django.conf.urls import patterns, include, url
#from django.contrib.contenttypes.models import ContentType


#Crud = CrudView(ContentType)

#urlpatterns = Crud.AsUrl(TemplateUpdate = 'controle_acesso.html')
urlpatterns = patterns('',
                       url('controle_acesso', 'parametro.controle_acesso.views.PaginaPrincipal'),
                       url('get_permissoes/', 'parametro.controle_acesso.views.GetPermissoes'),
                       url('set_permissoes/', 'parametro.controle_acesso.views.SetPermissoes'),
                    )