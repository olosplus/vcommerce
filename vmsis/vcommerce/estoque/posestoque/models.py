# -*- coding: utf-8 -*-
from django.db import models
from cadastro.produto.models import Produto
from estoque.lote.models import Lote
from cadastro.almoxarifado.models import Almoxarifado
from vlib.control.models import Master_unidade

# Create your models here.
class Posestoque(Master_unidade):
	class Meta:
		db_table = "posestoque"
		verbose_name = "Posição de Estoque"
		verbose_name_plural = "Posições de Estoque"

	produto = models.ForeignKey(Produto,verbose_name='Produto')
	almoxarifado = models.ForeignKey(Almoxarifado,verbose_name='Almoxarifado')
	#lote = models.ForeignKey(Lote,verbose_name='Lote')
	qtdeproduto = models.FloatField(verbose_name='Quantidade')