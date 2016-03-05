# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from financeiro.cartao_bandeira.models import Cartao_Bandeira

Crud = CrudView(Cartao_Bandeira)

urlpatterns = Crud.AsUrl(GridFields  = ('nmbandeira','qtdias_cred','qtdias_deb','idativo'))