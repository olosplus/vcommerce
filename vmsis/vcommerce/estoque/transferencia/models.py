# -*- coding: utf-8 -*-
from django.db import models
from vlib.vmodels import widgets
from estoque.control.models import Master_moviest
from cadastro.almoxarifado.models import Almoxarifado

# Create your models here.
class Transferencia(Master_moviest):
	class Meta:
		db_table = "transferencia"
		verbose_name = "Transferência"
		verbose_name_plural = "Transferências"
		child_models = ['estoque.transferencia.itemtransf.models.Itemtransf']
		ordering = ['-id']

	dttransferencia = widgets.VDateField(auto_now_add=True, verbose_name='Data de Entrada')
	to_almoxarifado = models.ForeignKey(Almoxarifado,related_name='almoxa_origem', verbose_name='Almoxarifado origem')
	from_almoxarifado = models.ForeignKey(Almoxarifado,related_name='almoxa_destino', verbose_name='Almoxarifado destino')

	def __str__(self):
		return self.dttransferencia