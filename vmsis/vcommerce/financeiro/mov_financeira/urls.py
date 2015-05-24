# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from financeiro.mov_financeira.models import Mov_Financeira

Crud = CrudView(Mov_Financeira)

urlpatterns = Crud.AsUrl(GridFields  = ('conta_destino','conta_origem','vlmovimentacao'))