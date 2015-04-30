# -*- coding: utf-8 -*-
from django.db import models
from cadastro.cliente.models import Cliente
from pedido.cadastro_pedido.mesa.models import Mesa
from pedido.cadastro_pedido.categoria.models import Categoria, ItemCategoria
from cadastro.produto.item.models import Item
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional, Adicionais
from pedido.cadastro_pedido.cardapio.models import Cardapio

choice_tipo_pedido = (('B','Balcao'),('D','Delivery'),('M','Mesa'))

choice_status_pedido = (('P','Pendente'),('C','Concluido'))

choice_SN = (('S','Sim'),('N','Não'))

# Create your models here.
class Pedido(models.Model):
	class Meta:
		db_table = "pedido"
		verbose_name = "Pedido"
		verbose_name_plural = "Pedidos"
		child_models = ['ItemPedido']

	idtipopedido = models.CharField(max_length=1,verbose_name="Tipo",choices=choice_tipo_pedido,default='B')
	cliente = models.ForeignKey(Cliente, verbose_name="Cliente",blank=True,null=True)
	nmcliente = models.CharField(max_length=250,verbose_name="Nome",blank=True,null=True)
	mesa = models.ForeignKey(Mesa, verbose_name="Mesa",blank=True,null=True)
	vrpedido = models.FloatField(verbose_name="Valor Total")
	idstatusped = models.CharField(max_length=1, verbose_name="Status",choices=choice_status_pedido,default='P')
	
class ItemPedido(models.Model):
	#class Meta:
	#	db_table="itempedido"
	#	child_models = ['ItAdicional']
	
	#categoria = models.ForeignKey(Categoria, verbose_name="Categoria")
	cardapio = models.ForeignKey(Cardapio, verbose_name="Item")
	qtitem = models.FloatField(verbose_name="Quantidade")
	vrvenda = models.ForeignKey(Cardapio, related_name='Preço', verbose_name="Valor Item")
	vrtotal = models.FloatField(verbose_name="Valor Total")
	idadicional = models.CharField(max_length=1,verbose_name="Adicional?",choices=choice_SN,default='N')

#class ItAdicional(models.Model):
	#adicional = models.ForeignKey(Adicionais, verbose_name="Adicional")