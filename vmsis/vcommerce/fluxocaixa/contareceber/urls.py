# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from fluxocaixa.contareceber.models import ContaReceber
from fluxocaixa.contareceber.views import ViewContaReceber

Crud = CrudView(ContaReceber)

urlpatterns = Crud.AsUrl(ClassCreate = ViewContaReceber)