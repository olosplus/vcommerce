 #-*- coding: utf-8 -*-
from django.db import models
from cadastro.produto.item.models import Item
from cadastro.produto.unimedida.models import Unimedida
from cadastro.empresa.models import Empresa


# Create your models here.
class ComposicaoProd(models.Model):
	class Meta:
		db_table = "ComposicaoProd"
		verbose_name = "Composição do produto"
		verbose_name_plural = "Composições dos produtos"
	
	item = models.ForeignKey(Item)
	prodcomp = models.ForeignKey(Item,  related_name='Produto', verbose_name='Produto')
	qtcomp = models.FloatField(verbose_name="Quantidade")
	unimedida = models.ForeignKey(Unimedida,verbose_name='Unidade de medida')
	#empresa = models.ForeignKey(Empresa,verbose_name="Empresa",null=True)

	