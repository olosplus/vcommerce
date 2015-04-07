 # -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.localidade.endereco.models import Endereco

Crud = CrudView(Endereco)

urlpatterns = Crud.AsUrl()