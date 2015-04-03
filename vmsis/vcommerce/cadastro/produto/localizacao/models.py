# -*- coding: utf-8 -*-
from django.db import models
from cadastro.produto.item.models import Item
from cadastro.almoxarifado.models import Almoxarifado
from cadastro.empresa.models import Empresa

# Create your models here.
class Localizacao(models.Model):
	class Meta:
		db_table = "localizacao"
		verbose_name = "Localização"
		verbose_name_plural = "Localizações"

	produto = models.ForeignKey(Item,verbose_name='Produto')
	almoxarifado = models.ForeignKey(Almoxarifado,verbose_name='Almoxarifado')
	dslocalizacao = models.CharField(max_length=400,verbose_name='Descrição',blank=True)
	empresa = models.ForeignKey(Empresa,verbose_name="Empresa")

	def __str__(self):
		return self.dslocalizacao