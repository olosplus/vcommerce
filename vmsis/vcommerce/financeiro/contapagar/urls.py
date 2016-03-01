# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from financeiro.contapagar.models import ContaPagar
Crud = CrudView(ContaPagar)

urlpatterns = Crud.AsUrl(GridFields  = ('idstatus', 'nro_documento', 'fornecedor_id', 'data_inclusao', 'data_prevista', 'valor_previsto', 'acrescimo', 'desconto', 'forma_pgto', 'data_baixa', 'valor_baixado', 'idorigem'))