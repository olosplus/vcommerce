# coding=UTF-8
from django.db import models
from financeiro.banco.models import Banco
from vlib.control.models import Master_unidade

# Create your models here.
class Conta(Master_unidade):
	class Meta:
		db_table = "conta"
		verbose_name = "Conta"
		verbose_name_plural = "Contas"
		ordering = ['banco','nragencia','nrconta']

	banco = models.ForeignKey(Banco,verbose_name="Banco")
	nragencia = models.CharField(max_length=30,verbose_name="Agencia")
	nrconta = models.CharField(max_length=30,verbose_name="Numero")
	vlsaldo = models.FloatField(verbose_name="Saldo")

	def __str__(self):
		return self.nrconta