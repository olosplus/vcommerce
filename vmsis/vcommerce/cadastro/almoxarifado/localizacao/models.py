# -*- coding: utf-8 -*-
from django.db import models
from cadastro.produto.models import Produto
from cadastro.almoxarifado.models import Almoxarifado
from vlib.control.models import Master_empresa

# Create your models here.
class Localizacao(Master_empresa):
	class Meta:
		db_table = "localizacao"
		verbose_name = "Localização"
		verbose_name_plural = "Localizações"

	produto = models.ForeignKey(Produto,verbose_name='Produto')
	almoxarifado = models.ForeignKey(Almoxarifado,verbose_name='Almoxarifado')
	dslocalizacao = models.CharField(max_length=400,verbose_name='Descrição',blank=True)

	def __str__(self):
		return self.dslocalizacao