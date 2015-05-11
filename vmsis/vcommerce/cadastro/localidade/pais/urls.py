# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.localidade.pais.models import Pais

Crud = CrudView(Pais)

urlpatterns = Crud.AsUrl(GridFields  = ('cdpais','nmpais','sgpais2','sgpais3',))