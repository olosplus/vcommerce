# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.almoxarifado.models import Almoxarifado

Crud = CrudView(Almoxarifado)

urlpatterns = Crud.AsUrl(GridFields  = ('nmalmoxa',))