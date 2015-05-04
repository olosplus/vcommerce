# -*- coding: utf-8 -*-
from django.db import models
from cadastro.unimedida.models import Unimedida
from vlib.control.models import Master_empresa

# Create your models here.
class Produto(Master_empresa):
	class Meta:
		db_table = "produto"
		verbose_name = "Produto"
		verbose_name_plural = "Produtos"
		child_models = ['pedido.cadastro_pedido.composicaoproduto.models.ComposicaoProd']


	posarvore = models.CharField(max_length=40,verbose_name='Arvore')
	nmproduto = models.CharField(max_length=200,verbose_name='Nome',blank=True)
	unimedida = models.ForeignKey(Unimedida,verbose_name='Unidade de medida')
	fatorconv = models.FloatField(verbose_name='Fator de conversão')
	cdbarra = models.CharField(max_length=100,verbose_name='Código de barras',blank=True)
	idprodvenda = models.BooleanField(verbose_name='Produto de venda',default=False,blank=True) 
	idadicional = models.BooleanField(verbose_name='Adicional',default=False,blank=True)

	def __str__(self):
		return self.nmproduto