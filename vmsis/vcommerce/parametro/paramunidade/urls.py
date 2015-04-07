# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from parametro.paramunidade.models import Paramunidade

Crud = CrudView(Paramunidade)

urlpatterns = Crud.AsUrl()