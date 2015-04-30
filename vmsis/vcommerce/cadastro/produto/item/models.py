# -*- coding: utf-8 -*-
from django.db import models
from cadastro.produto.unimedida.models import Unimedida
from cadastro.empresa.models import Empresa

# Create your models here.
class Item(models.Model):
	class Meta:
		db_table = "produto"
		verbose_name = "Produto"
		verbose_name_plural = "Produtos"
		child_models = ['pedido.cadastro_pedido.composicaoproduto.models.ComposicaoProd']


	posarvore = models.CharField(max_length=40,verbose_name='Arvore')
	nmproduto = models.CharField(max_length=200,verbose_name='Nome',blank=True)
	unimedida = models.ForeignKey(Unimedida,verbose_name='Unidade de medida')
	#prodcmp = models.OneToOneField('self',related_name='Produto_prodcmp',verbose_name='Produto de compra')
	#prodest = models.OneToOneField('self',related_name='Produto_prodest',verbose_name='Produto de estoque')
	fatorconv = models.FloatField(verbose_name='Fator de conversão')
	cdbarra = models.CharField(max_length=100,verbose_name='Código de barras',blank=True)
	idprodvenda = models.BooleanField(verbose_name='Produto de venda',default=False,blank=True) 
	idadicional = models.BooleanField(verbose_name='Adicional',default=False,blank=True)
	empresa = models.ForeignKey(Empresa,verbose_name="Empresa",null=True)

	def __str__(self):
		return self.nmproduto