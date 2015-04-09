# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from cadastro.localidade.bairro.models import Bairro

Crud = CrudView(Bairro)

urlpatterns = Crud.AsUrl()#GridFields  = ('cdibge','nmbairro',))