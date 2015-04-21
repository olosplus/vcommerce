# coding=UTF-8
from django.db import models
from financeiro.banco.models import Banco
from cadastro.unidade.models import Unidade

# Create your models here.
class Conta(models.Model):
	class Meta:
		db_table = "conta"
		verbose_name = "Conta"
		verbose_name_plural = "Contas"

	banco = models.ForeignKey(Banco,verbose_name="Banco")
	nragencia = models.CharField(max_length=30,verbose_name="Agencia")
	nrconta = models.CharField(max_length=30,verbose_name="Numero")
	vlsaldo = models.FloatField(verbose_name="Saldo")
	unidade = models.ForeignKey(Unidade,verbose_name="Unidade", null=True, blank=True)

	def __str__(self):
		return self.nrconta