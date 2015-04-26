# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from estoque.cadastro_estoque.finalidade.models import Finalidade

Crud = CrudView(Finalidade)

urlpatterns = Crud.AsUrl(GridFields  = ('descricao','unidade__nmfantasia',))