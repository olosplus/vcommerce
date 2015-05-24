# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.pedido.models import Pedido

Crud = CrudView(Pedido)

urlpatterns = Crud.AsUrl()
