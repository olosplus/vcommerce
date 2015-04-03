# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.localidade.estado.models import Estado

Crud = CrudView(Estado)

urlpatterns = Crud.AsUrl()