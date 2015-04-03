# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.cliente.models import Cliente

Crud = CrudView(Cliente)

urlpatterns = Crud.AsUrl(GridFields  = ('nrinscjurd','nmcliente',))