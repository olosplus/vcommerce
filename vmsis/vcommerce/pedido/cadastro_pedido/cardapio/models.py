# -*- coding: utf-8 -*-
from django.db import models
#from pedido.cadastro_pedido.categoria.models import Categoria, ItemCategoria
from cadastro.produto.models import Produto
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional

choice_tipo_ativ = (('A','Ativa'),
	('D','Inativa'))

choice_SN = (('S','Sim'),
	('N','Não'))

# Create your models here.
class Cardapio(models.Model):
	class Meta:
		db_table = "cardapio"
		verbose_name = "Cardapio"
		verbose_name_plural = "Cardapios"
		child_models = ['ItAgrupAdicional']

	#nmcategoria = models.CharField(max_length=250,verbose_name="Nome",unique=True)
	#idcardapiotiv = models.CharField(max_length=1,verbose_name="Situação",choices=choice_tipo_ativ,default='A')
	#categoria = models.ForeignKey(Categoria, verbose_name="Categoria")
	produto = models.ForeignKey(Produto, verbose_name="Produto")
	vrvenda = models.FloatField(verbose_name="Preço")
	idadicional = models.CharField(max_length=1,verbose_name="Permite Adicionais?",choices=choice_SN,default='N')
	
	def __str__(self):
		return self.produto.nmproduto

class ItAgrupAdicional(models.Model):
	class Meta:
		db_table = "itagrupadicional"
		verbose_name = "Agrupamentos de Adicionais Permitidos"
		verbose_name_plural = "Agrupamentos de Adicionais Permitidos"
	cardapio = models.ForeignKey(Cardapio)
	agrupadicional = models.ForeignKey(AgrupAdicional, verbose_name="Agrupamentos de Adicionais")