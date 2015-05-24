# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from fluxocaixa.contapagar.models import ContaPagar
from fluxocaixa.contapagar.views import ViewContaPagar

Crud = CrudView(ContaPagar)

urlpatterns = Crud.AsUrl(ClassCreate = ViewContaPagar)