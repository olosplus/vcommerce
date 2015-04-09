# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.produto.localizacao.models import Localizacao

Crud = CrudView(Localizacao)

urlpatterns = Crud.AsUrl(GridFields  = ('almoxarifado','dslocalizacao',))