# -*- coding: utf-8 -*-
from django.db import models
from estoque.control.models import Master_moviest
from cadastro.produto.models import Produto
from cadastro.almoxarifado.models import Almoxarifado
from estoque.lote.models import Lote
from vlib.control.models import Master_empresa

# Create your models here.
class Itemtransf(Master_empresa):
	class Meta:
		db_table = "itemtransf"
		verbose_name = "Item"
		verbose_name_plural = "Itens"
		ordering = ['produto__nmproduto']
	
	produto = models.ForeignKey(Produto,verbose_name='Produto')
	lote = models.ForeignKey(Lote,related_name='lote',verbose_name='Lote', null=True, blank=True)
	qtdeprod = models.FloatField(verbose_name="Quantidade")
	master_moviest = models.ForeignKey(Master_moviest,null=True)