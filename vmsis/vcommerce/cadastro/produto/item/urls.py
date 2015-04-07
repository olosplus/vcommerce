# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.produto.item.models import Item

Crud = CrudView(Item)

urlpatterns = Crud.AsUrl()