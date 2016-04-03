# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from pedido.frentecaixa.models import Pedido

crud = CrudView(Pedido)
urlpatterns = crud.AsUrl()

#urlpatterns = patterns('',
#                       url('pedido', 'pedido.frentecaixa.views.CarregarPedido'),
#                    )
