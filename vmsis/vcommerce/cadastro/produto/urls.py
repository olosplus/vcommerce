# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.produto.models import Produto
from cadastro.produto.views import CreateProduto, UpdateProduto

Crud = CrudView(Produto)

urlpatterns = Crud.AsUrl(GridFields  = ('nmproduto','unimedida__sgmedida','cdbarra',), MediaFilesInsert=['produto/produto.js'],
                         MediaFilesUpdate=['produto/produto.js'], ClassCreate=CreateProduto, ClassUpdate=UpdateProduto)