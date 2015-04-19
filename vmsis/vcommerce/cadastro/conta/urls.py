# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.conta.models import Conta

Crud = CrudView(Conta)

urlpatterns = Crud.AsUrl(GridFields  = ('nragencia','nrconta','vlsaldo'))