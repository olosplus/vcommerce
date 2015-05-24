 #-*- coding: utf-8 -*-
from django.db import models
from cadastro.produto.models import Produto
from cadastro.unimedida.models import Unimedida
from cadastro.empresa.models import Empresa

# Create your models here.
class ComposicaoProd(models.Model):
	class Meta:
		db_table = "ComposicaoProd"
		verbose_name = "Composição do produto"
		verbose_name_plural = "Composições dos produtos"
	
	produto = models.ForeignKey(Produto)
	prodcomp = models.ForeignKey(Produto,  related_name='Produto', verbose_name='Produto')
	qtcomp = models.FloatField(verbose_name="Quantidade")
	unimedida = models.ForeignKey(Unimedida,verbose_name='Unidade de medida')