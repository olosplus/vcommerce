# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_unidade

# Create your models here.
class Lote(Master_unidade):
	class Meta:
		db_table = "lote"
		verbose_name = "Lote"
		verbose_name_plural = "Lotes"

	dslote = models.CharField(max_length=100,verbose_name='Lote')
	dtvalidade = models.DateField(verbose_name='Data de Validade')
	dtfabricacao = models.DateField(verbose_name='Data de Fabricação')

	def __str__(self):
		return self.dslote