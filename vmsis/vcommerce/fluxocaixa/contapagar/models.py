# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_unidade
from cadastro.fornecedor.models import Fornecedor

choice_forma_pagamento = (
    ('B','Boleto'),
	('C','Cheque'),
	('D','Depósito'),
    ('I', 'Dinheiro'))

choice_repetir = (
    ('1', 'Uma Vez'),
    ('2', 'Diariamente'),
    ('3', 'Semanalmente'),
    ('4', 'Quinzenalmente'),
    ('5', 'Mensalmente'),
    ('6', 'Trimestralmente'),
    ('7', 'Anualmente'))

choice_status = (
    ('1', 'A Pagar'),
    ('2', 'Paga'))

# Create your models here.
class ContaPagar(Master_unidade):
    class Meta:
    	db_table = "contapagar"
    	verbose_name = "Conta a Pagar"
    	verbose_name_plural = "Conta a Pagar"

    idformapagamento = models.CharField(max_length=1,verbose_name="Forma de Pagamento",choices=choice_forma_pagamento)
    dscontapagar = models.CharField(max_length=2000,verbose_name="Descriçao")
    nrinscjurdForn = models.ForeignKey(Fornecedor, verbose_name="Forncedor")
    vrcontapagar = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Valor")
    dtvencimento = models.DateField(verbose_name="Vencimento")
    idrepetir = models.CharField(max_length=1,verbose_name="Repetir",choices=choice_repetir)
    dtfinal = models.DateField(verbose_name="Data Final")
    idstatus = models.CharField(max_length=1, verbose_name="Situação", choices=choice_status, default="1")
    idorigem = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
    	return self.descricao