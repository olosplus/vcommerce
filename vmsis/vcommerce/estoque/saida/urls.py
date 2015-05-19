# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from estoque.saida.models import Saida
from estoque.saida.views import ViewSaidaCreate, ViewSaidaUpdate

Crud = CrudView(Saida)

urlpatterns = Crud.AsUrl(ClassCreate = ViewSaidaCreate, ClassUpdate = ViewSaidaUpdate)