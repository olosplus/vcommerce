# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.localidade.cidade.models import Cidade

Crud = CrudView(Cidade)

urlpatterns = Crud.AsUrl()