# -*- coding: utf-8 -*-
from django.db import models
from cadastro.cliente.models import Cliente
from pedido.cadastro_pedido.mesa.models import Mesa
from pedido.cadastro_pedido.categoria.models import Categoria 
from cadastro.produto.models import Produto
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional, Adicionais
from pedido.cadastro_pedido.itemcategoria.models import ItemCategoria
from vlib.control.models import Master_empresa, ControleSincronizacao
from cadastro.almoxarifado.models import Almoxarifado
from estoque.lote.models import Lote

choice_tipo_pedido = (('B','Balcao'),('D','Delivery'),('M','Mesa'))

choice_status_pedido = (('F','Finalizado'),('C','Cancelado'), ('A', 'Aberto'))

choice_SN = (('S','Sim'),('N','Não'))

# Create your models here.
class Pedido(ControleSincronizacao):
	class Meta:
		db_table = "pedido"
		verbose_name = "Pedido"
		verbose_name_plural = "Pedidos"
		child_models = ['ItemPedido']

	idtipopedido = models.CharField(max_length=1,verbose_name="Tipo",choices=choice_tipo_pedido,default='B')
	cliente = models.ForeignKey(Cliente, verbose_name="Cliente",blank=True,null=True)
	nmcliente = models.CharField(max_length=250,verbose_name="Nome",blank=True,null=True)
	mesa = models.ForeignKey(Mesa, verbose_name="Mesa",blank=True,null=True)
	vrpedido = models.FloatField(verbose_name='Valor total',default=0,editable = False)
	idstatusped = models.CharField(max_length=1, default='P',
	    choices=choice_status_pedido)
	dsmotivo = models.TextField(verbose_name="Motivo para o cancelamento", null=True)

class ItemPedido(Master_empresa, ControleSincronizacao):
	class Meta:
		db_table = "itempedido"
		verbose_name = "Item do Pedido"
		verbose_name_plural = "Itens dos Pedidos"
		child_models = ['ItAdicional']

	pedido = models.ForeignKey(Pedido)
	cardapio = models.ForeignKey(ItemCategoria, verbose_name="Produto")
	almoxarifado = models.ForeignKey(Almoxarifado,verbose_name='Almoxarifado', editable=False)
	lote = models.ForeignKey(Lote,verbose_name='Lote', null=True, blank=True)
	qtitem = models.FloatField(verbose_name="Quantidade")
	vrvenda = models.FloatField(default=0,editable=False)
	vrtotal = models.FloatField(default=0,editable = False)
	idadicional = models.BooleanField(verbose_name='Adicional',default=False,blank=True)
	produto = models.ForeignKey(Produto, verbose_name="Produto")

class ItAdicional(ControleSincronizacao):
	class Meta:
		db_table = "ItAdicional"
		verbose_name = "Adicional do produto"
		verbose_name_plural = "Adicionais do produto"

	itempedido = models.ForeignKey(ItemPedido)
	item = models.ForeignKey(Adicionais, verbose_name="Produto")
	qtitem = models.FloatField(verbose_name="Quantidade")
	valor = models.FloatField(verbose_name="Valor")
	VrVenda = models.FloatField(verbose_name="Valor da venda")
