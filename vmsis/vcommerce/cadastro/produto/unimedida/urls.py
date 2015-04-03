# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.produto.unimedida.models import Unimedida

Crud = CrudView(Unimedida)

urlpatterns = Crud.AsUrl()