# coding=UTF-8
from django.db import models
from cadastro.banco.models import Banco

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

	def __str__(self):
		return self.nrconta