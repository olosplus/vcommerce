# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_unidade
from cadastro.cliente.models import Cliente

choice_forma_recebimento = (
    ('C', 'Crédito'),
    ('D', 'Débito'),
    ('M', 'Dinheiro'),
	('H','Cheque'),
	('T','Depósito'))

choice_status = (
    ('A', 'Em Eberto'),
    ('B', 'Baixado'))

# Create your models here.
class ContaReceber(Master_unidade):
    class Meta:
    	db_table = "contareceber"
    	verbose_name = "Conta a Receber"
    	verbose_name_plural = "Contas a Receber"

    nro_documento = models.CharField(max_length=10,verbose_name="Número Documento")
    cliente_id = models.ForeignKey(Cliente, verbose_name="Cliente")
    data_inclusao = models.DateField(verbose_name="Data Inclusão")
    data_prevista = models.DateField(verbose_name="Data Prevista")
    data_baixa = models.DateField(verbose_name="Data Baixa", null=True)
    valor_previsto = models.FloatField(verbose_name="Valor Previsto")
    acrescimo = models.FloatField(verbose_name="Acréscimo", null=True)
    desconto = models.FloatField(verbose_name="Desconto", null=True)
    valor_baixado = models.FloatField(verbose_name="Valor Baixado", null=True)
    idstatus = models.CharField(max_length=1, verbose_name="Situação", choices=choice_status, default="1")
    forma_rbto = models.CharField(max_length=1,verbose_name="Forma de Recebimento",choices=choice_forma_recebimento)
    idorigem = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
    	return self.nro_documento