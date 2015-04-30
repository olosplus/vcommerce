# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from pedido.cadastro_pedido.cardapio.models import Cardapio

Crud = CrudView(Cardapio)

urlpatterns = Crud.AsUrl()
