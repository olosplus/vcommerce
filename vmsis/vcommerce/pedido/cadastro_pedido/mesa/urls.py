# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from pedido.cadastro_pedido.mesa.models import Mesa


Crud = CrudView(Mesa)

urlpatterns = Crud.AsUrl()
