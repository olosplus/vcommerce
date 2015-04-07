# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from parametro.paramgeral.models import Paramgeral

Crud = CrudView(Paramgeral)

urlpatterns = Crud.AsUrl()