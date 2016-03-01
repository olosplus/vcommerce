# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_unidade
from cadastro.fornecedor.models import Fornecedor

choice_forma_pagamento = (
    ('C', 'Crédito'),
    ('D', 'Débito'),
    ('M', 'Dinheiro'),
	('H','Cheque'),
	('T','Depósito'))

choice_status = (
    ('A', 'Em Eberto'),
    ('B', 'Baixado'))

# Create your models here.
class ContaPagar(Master_unidade):
    class Meta:
    	db_table = "contapagar"
    	verbose_name = "Conta a Pagar"
    	verbose_name_plural = "Contas a Pagar"

    nro_documento = models.CharField(max_length=10,verbose_name="Número Documento")
    fornecedor_id = models.ForeignKey(Fornecedor, verbose_name="Fornecedor")
    data_inclusao = models.DateField(verbose_name="Data Inclusão")
    data_prevista = models.DateField(verbose_name="Data Prevista")
    data_baixa = models.DateField(verbose_name="Data Baixa", null=True)
    valor_previsto = models.FloatFIeld(verbose_name="Valor Previsto")
    acrescimo = models.FloatField(verbose_name="Acréscimo", null=True)
    desconto = models.FloatFIeld(verbose_name="Desconto", null=True)
    valor_baixado = models.FloatFIeld(verbose_name="Valor Baixado", null=True)
    idstatus = models.CharField(max_length=1, verbose_name="Situação", choices=choice_status, default="1")
    forma_pgto = models.CharField(max_length=1,verbose_name="Forma de Pagamento",choices=choice_forma_pagamento)
    idorigem = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
    	return self.nro_documento