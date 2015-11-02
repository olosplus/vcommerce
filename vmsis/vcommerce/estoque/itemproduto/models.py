# -*- coding: utf-8 -*-
from django.db import models
from estoque.control.models import Master_moviest
from cadastro.produto.models import Produto
from cadastro.almoxarifado.models import Almoxarifado
from estoque.lote.models import Lote
from vlib.control.models import Master_empresa, ControleSincronizacao

# Create your models here.
class Itemproduto(Master_empresa, ControleSincronizacao):
	class Meta:
		db_table = "itemproduto"
		verbose_name = "Item"
		verbose_name_plural = "Itens"
		ordering = ['-id']
	
	produto = models.ForeignKey(Produto,verbose_name='Produto')
	almoxarifado = models.ForeignKey(Almoxarifado,verbose_name='Almoxarifado')
	lote = models.ForeignKey(Lote,verbose_name='Lote', null=True, blank=True)
	qtdeprod = models.FloatField(verbose_name="Quantidade")
	master_moviest = models.ForeignKey(Master_moviest,null=True)
	vlProd = models.FloatField("Valor unitário")