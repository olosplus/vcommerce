# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from financeiro.banco.models import Banco

Crud = CrudView(Banco)

urlpatterns = Crud.AsUrl()