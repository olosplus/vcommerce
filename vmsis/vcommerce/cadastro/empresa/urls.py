 # -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.empresa.models import Empresa
from cadastro.empresa.views import ViewEmpresa

Crud = CrudView(Empresa)

urlpatterns = Crud.AsUrl(ClassCreate = ViewEmpresa)