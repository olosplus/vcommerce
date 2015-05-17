# coding=UTF-8
from django.db import models
from financeiro.conta.models import Conta
from vlib.control.models import Master_unidade
from cadastro.centro_custo.models import CentroCusto

# Create your models here.

class Mov_Financeira(Master_unidade):
	class Meta:
		db_table = "mov_financeira"
		verbose_name = "Movimentaçao Financeira"

	tipo = models.CharField(max_length = 1, verbose_name="Tipo")
	origem = models.CharField(max_length=1,verbose_name="Origem")
	conta_destino = models.ForeignKey(Conta, related_name='conta_destino',verbose_name="Conta")
	conta_origem = models.ForeignKey(Conta, related_name='conta_origem',verbose_name="Conta Origem", null=True)
	vlmovimentacao = models.FloatField(verbose_name="Valor")
	observacao = models.CharField(max_length=150,verbose_name="Observaçao",blank=True)
	centro_custo = models.ForeignKey(CentroCusto, verbose_name="Centro de custo")
