# -*- coding: utf-8 -*-
from django.db import models
from cadastro.produto.models import Produto

choice_tipo_ativ = (('A','Ativa'),
	('D','Inativa'))

# Create your models here.
class AgrupAdicional(models.Model):
	class Meta:
		db_table = "AgrupAdicional"
		verbose_name = "Agrupamento de Adicional"
		verbose_name_plural = "Agrupamentos de Adicionais"
		child_models = ['Adicionais']

	nmagrupadic = models.CharField(max_length=250,verbose_name="Nome",unique=True)
	vragrupadic = models.FloatField(verbose_name="Valor do agrupamento")
	idagrupativ = models.CharField(max_length=1,verbose_name="Situação",choices=choice_tipo_ativ,default='A')
	def __str__(self):
		return self.nmagrupadic

class Adicionais(models.Model):
	class Meta:
		db_table = "Adicionais"
		
	agrupadicional = models.ForeignKey(AgrupAdicional)
	item = models.ForeignKey(Produto, verbose_name="Adicional")
	valor = models.FloatField(verbose_name="Valor")
	quantidade = models.FloatField(verbose_name="Quantidade")
	def __str__(self):
		return self.item.nmproduto


