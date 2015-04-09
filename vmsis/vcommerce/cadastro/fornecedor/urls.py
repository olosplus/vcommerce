# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.fornecedor.models import Fornecedor

Crud = CrudView(Fornecedor)

urlpatterns = Crud.AsUrl(GridFields  = ('nrinscjurd','nmfornecedor',))