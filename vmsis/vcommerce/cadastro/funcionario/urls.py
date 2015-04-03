 # -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.funcionario.models import Funcionario

Crud = CrudView(Funcionario)

urlpatterns = Crud.AsUrl(GridFields  = ('nome','usuario','unidade',))