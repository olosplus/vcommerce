# -*- coding: utf-8 -*-
from django.db import models
from estoque.control.models import Master_moviest
from cadastro.produto.models import Produto
from cadastro.almoxarifado.models import Almoxarifado
from estoque.lote.models import Lote
from vlib.control.models import Master_empresa

# Create your models here.
class Iteminvent(Master_empresa):
	class Meta:
		db_table = "iteminvent"
		verbose_name = "Item"
		verbose_name_plural = "Itens"
		ordering = ['produto__nmproduto']
	
	produto = models.ForeignKey(Produto,verbose_name='Produto')
	almoxarifado = models.ForeignKey(Almoxarifado,verbose_name='Almoxarifado')
	lote = models.ForeignKey(Lote,verbose_name='Lote', null=True, blank=True)
	qtdeprod_old = models.FloatField(verbose_name="Qdte Anterior")
	qtdeprod = models.FloatField(verbose_name="Quantidade")
	master_moviest = models.ForeignKey(Master_moviest,null=True)