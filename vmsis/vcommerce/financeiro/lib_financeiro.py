# -*- coding: utf-8 -*-
from django.db import models 
from django.db.models import Sum
from financeiro.cartao_bandeira.models import Cartao_Bandeira
from financeiro.contareceber.models import ContaReceber


def addCAR(p_origem, p_data, p_cliente, p_doc, p_valor, p_forma_rbto, p_bandeira, p_unidade):
	data = p_data
	if p_bandeira<>0:
	    bandeira = Cartao_Bandeira.objects.get(pk=p_bandeira)
		if p_forma_rbto='D':
		    data += bandeira.qtdias_deb
		elif p_forma_rbto='C':
		    data += bandeira.qtdias_cred 
	
	car = ContaReceber.objects.create(
		unidade_id = p_unidade,
		cliente_id = p_cliente,
		data_inclusao = p_data,
		data_prevista = data,
		nro_documento = p_doc,
		valor_previsto = p_valor,
		forma_rbto = p_forma_rbto,
		idstatus = 'A',
		idorigem = p_origem
	)