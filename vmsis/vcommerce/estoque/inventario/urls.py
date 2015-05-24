# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from estoque.inventario.models import Inventario
from estoque.inventario.views import ViewInventarioCreate, ViewInventarioUpdate

Crud = CrudView(Inventario)

urlpatterns = Crud.AsUrl(ClassCreate = ViewInventarioCreate, ClassUpdate = ViewInventarioUpdate,
	GridFields  = ('dtinventario','almoxarifado__nmalmoxa'), MediaFilesUpdate = ['js/inventario_upd.js'],
	MediaFilesInsert = ['js/inventario_ins.js'])