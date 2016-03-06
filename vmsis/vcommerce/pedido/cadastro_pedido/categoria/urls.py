# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from pedido.cadastro_pedido.categoria.models import Categoria
from pedido.cadastro_pedido.categoria.views import CreateCategoria, UpdateCategoria

Crud = CrudView(Categoria)

urlpatterns = Crud.AsUrl(ClassCreate = CreateCategoria, ClassUpdate = UpdateCategoria, MediaFilesInsert = ['categoria/categoria.js', 'categoria/categoria.css'],
                         MediaFilesUpdate = ['categoria/categoria.js', 'categoria/categooria.css'])
