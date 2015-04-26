# -*- coding: utf-8 -*-
from django.db import models
from estoque.control.models import Movimentacaoest
from cadastro.produto.item.models import Item
from cadastro.almoxarifado.models import Almoxarifado

# Create your models here.
class Itemproduto(models.Model):
	class Meta:
		db_table = "itemproduto"
		verbose_name = "Item"
		verbose_name_plural = "Itens"
	
	produto = models.ForeignKey(Item,verbose_name='Produto')
	almoxarifado = models.ForeignKey(Almoxarifado,verbose_name='Almoxarifado')	
	qtdeprod = models.FloatField(verbose_name="Quantidade")
	master = models.ForeignKey(Movimentacaoest)