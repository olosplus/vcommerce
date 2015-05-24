# coding=UTF-8
from django.db import models
from financeiro.conta.models import Conta
from cadastro.unidade.models import Unidade
from cadastro.centro_custo.models import

# Create your models here.
class Mov_Financeira(models.Model):
	class Meta:
		db_table = "mov_financeira"
		verbose_name = "Movimentacao Financeira"

		unidade = models.ForeignKey(Unidade,verbose_name="Unidade", null=True, blank=True)
		conta = models.ForeignKey(Conta,verbose_name="Conta")
		#centrocusto = models.ForeignKey(CentroCusto,verbose_name="Centro de Custo")