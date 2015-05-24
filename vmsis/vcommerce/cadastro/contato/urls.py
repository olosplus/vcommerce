 # -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.contato.models import Contato

Crud = CrudView(Contato)

urlpatterns = Crud.AsUrl(GridFields  = ('nmcontato','nrtelefone','nrcelular','dsemail',))