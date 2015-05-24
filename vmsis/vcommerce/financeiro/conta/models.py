# coding=UTF-8
from django.db import models
<<<<<<< HEAD:vmsis/vcommerce/financeiro/conta/models.py
from financeiro.banco.models import Banco
from cadastro.unidade.models import Unidade
=======
from cadastro.banco.models import Banco
from vlib.control.models import Master_empresa
>>>>>>> 2bfa5d457b5fcdbd10b45ea522f1fc26f937891a:vmsis/vcommerce/cadastro/conta/models.py

# Create your models here.
class Conta(Master_empresa):
	class Meta:
		db_table = "conta"
		verbose_name = "Conta"
		verbose_name_plural = "Contas"
		ordering = ['banco','nragencia','nrconta']

	banco = models.ForeignKey(Banco,verbose_name="Banco")
	nragencia = models.CharField(max_length=30,verbose_name="Agencia")
	nrconta = models.CharField(max_length=30,verbose_name="Numero")
	vlsaldo = models.FloatField(verbose_name="Saldo")
	unidade = models.ForeignKey(Unidade,verbose_name="Unidade", null=True, blank=True)

	def __str__(self):
		return self.nrconta