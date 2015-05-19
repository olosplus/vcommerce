# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from estoque.entrada.models import Entrada
from estoque.entrada.views import ViewEntradaCreate, ViewEntradaUpdate

Crud = CrudView(Entrada)

urlpatterns = Crud.AsUrl(ClassCreate = ViewEntradaCreate, ClassUpdate = ViewEntradaUpdate)