# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from estoque.lote.models import Lote

Crud = CrudView(Lote)

urlpatterns = Crud.AsUrl(GridFields  = ('dslote','dtvalidade',))