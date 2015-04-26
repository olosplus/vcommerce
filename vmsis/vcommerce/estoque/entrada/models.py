# -*- coding: utf-8 -*-
from django.db import models
from estoque.control.models import Master_moviest
from cadastro.fornecedor.models import Fornecedor

# Create your models here.
class Entrada(Master_moviest):
	class Meta:
		db_table = "entrada"
		verbose_name = "Entrada"
		verbose_name_plural = "Entradas"
		child_models = ['estoque.itemproduto.models.Itemproduto']

	dtentrada = models.DateTimeField(verbose_name='Data de Entrada')
	fornecedor = models.ForeignKey(Fornecedor,verbose_name='Fornecedor')