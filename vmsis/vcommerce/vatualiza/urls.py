# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from vatualiza.models import Vatualiza

Crud = CrudView(Vatualiza)

urlpatterns = Crud.AsUrl(GridFields  = ('resumo','versao','dtatualiza',))