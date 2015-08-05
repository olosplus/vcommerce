# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from pedido.itemreti.models import ItemReti
from pedido.itemreti.views import ViewItemretiCreate, ViewItemretiUpdate


Crud = CrudView(ItemReti)

urlpatterns = Crud.AsUrl()
urlpatterns = Crud.AsUrl(ClassCreate = ViewItemretiCreate,ClassUpdate = ViewItemretiUpdate)
