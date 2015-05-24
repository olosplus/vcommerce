# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from pedido.frentecaixa.models import Pedido
from pedido.frentecaixa.views import ViewFrentecaixaCreate


Crud = CrudView(Pedido)

urlpatterns = Crud.AsUrl(MediaFilesInsert = ['js/pedido.js'],ClassCreate = ViewFrentecaixaCreate,GridFields  = ('idtipopedido','vrpedido'))