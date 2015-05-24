 # -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.funcionario.models import Funcionario
from cadastro.funcionario.views import ViewFuncionario

Crud = CrudView(Funcionario)

urlpatterns = Crud.AsUrl(GridFields  = ('nome','usuario',), ClassCreate = ViewFuncionario)