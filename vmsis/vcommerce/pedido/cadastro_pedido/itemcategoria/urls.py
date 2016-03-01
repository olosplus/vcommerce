# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView

from pedido.cadastro_pedido.itemcategoria.models import ItemCategoria

Crud = CrudView(ItemCategoria)

urlpatterns = Crud.AsUrl(GridFields = ['categoria__nmcategoria', 'produto__nmproduto'], MediaFilesList=['itemcategoria/itemcategoria.js'])
urlpatterns += patterns('', url(r'^itemcategoria/relagrupamento', 'pedido.cadastro_pedido.itemcategoria.views.RelCardapio' ),)
urlpatterns += patterns('', url(r'^itemcategoria/relagrupamento', 'pedido.cadastro_pedido.itemcategoria.views.RelCardapio' ),)
