# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional

Crud = CrudView(AgrupAdicional)

urlpatterns = Crud.AsUrl()
