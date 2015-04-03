 # -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.unidade.models import Unidade

Crud = CrudView(Unidade)

urlpatterns = Crud.AsUrl() 