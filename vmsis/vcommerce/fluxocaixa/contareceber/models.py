# -*- coding: utf-8 -*-
from django.db import models
from cadastro.empresa.models import Empresa
from cadastro.unidade.models import Unidade
from cadastro.cliente.models import Cliente

choice_forma_recebimento = (
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
    ('1', 'A Receber'),
    ('2', 'Recebido'))

# Create your models here.
class ContaReceber(models.Model):
    class Meta:
    	db_table = "contareceber"
    	verbose_name = "Conta a Receber"
    	verbose_name_plural = "Conta a Receber"

    cdempresa = models.ForeignKey(Empresa, verbose_name="Empresa")
    nrinscjurdUnid = models.ForeignKey(Unidade, verbose_name="Unidade")
    idformapagamento = models.CharField(max_length=1,verbose_name="Forma de Recebimento",choices=choice_forma_recebimento)
    dscontareceber = models.CharField(max_length=2000,verbose_name="Descriçao")
    nrinscjurdClie = models.ForeignKey(Cliente, verbose_name="Cliente")
    vrcontareceber = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Valor")
    dtvencimento = models.DateField(verbose_name="Vencimento")
    idrepetir = models.CharField(max_length=1,verbose_name="Repetir",choices=choice_repetir)
    dtfinal = models.DateField(verbose_name="Data Final")
    idstatus = models.CharField(max_length=1, verbose_name="Situação", choices=choice_status, default="1")
    idorigem = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
    	return self.descricao