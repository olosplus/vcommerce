# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from pedido.movcaixa.models import MovCaixa

Crud = CrudView(MovCaixa)

urlpatterns = Crud.AsUrl()