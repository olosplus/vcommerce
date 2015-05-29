# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from estoque.transferencia.models import Transferencia
from estoque.transferencia.views import ViewTransferenciaCreate, ViewTransferenciaUpdate

Crud = CrudView(Transferencia)

urlpatterns = Crud.AsUrl(ClassCreate = ViewTransferenciaCreate, ClassUpdate = ViewTransferenciaUpdate, 
	GridFields = ('dttransferencia','to_almoxarifado__nmalmoxa','from_almoxarifado__nmalmoxa'))