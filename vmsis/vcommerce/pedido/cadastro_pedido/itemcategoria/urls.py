# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from pedido.cadastro_pedido.itemcategoria.models import ItemCategoria

Crud = CrudView(ItemCategoria)

urlpatterns = Crud.AsUrl()
