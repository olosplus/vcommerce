# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from estoque.entrada.models import Entrada

Crud = CrudView(Entrada)

urlpatterns = Crud.AsUrl()