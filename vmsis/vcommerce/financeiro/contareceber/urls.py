# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from financeiro.contareceber.models import ContaReceber

Crud = CrudView(ContaReceber)

urlpatterns = Crud.AsUrl(GridFields  = ('idstatus', 'nro_documento', 'cliente_id', 'data_inclusao', 'data_prevista', 'valor_previsto', 'acrescimo', 'desconto', 'forma_rbto', 'data_baixa', 'valor_baixado', 'idorigem'))