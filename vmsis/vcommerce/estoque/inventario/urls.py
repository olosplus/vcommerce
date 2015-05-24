# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from estoque.inventario.models import Inventario
from estoque.inventario.views import ViewInventario

Crud = CrudView(Inventario)

urlpatterns = Crud.AsUrl(ClassCreate = ViewInventario)