# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.produto.models import Produto

Crud = CrudView(Produto)

urlpatterns = Crud.AsUrl(GridFields  = ('posarvore','nmproduto','unimedida',))