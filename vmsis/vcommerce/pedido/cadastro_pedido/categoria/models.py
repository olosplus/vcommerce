# -*- coding: utf-8 -*-
from django.db import models
from cadastro.produto.item.models import Item

choice_tipo_ativ = (('A','Ativa'),
	('D','Inativa'))


# Create your models here.
class Categoria(models.Model):
	class Meta:
		db_table = "categoria"
		verbose_name = "Categoria"
		verbose_name_plural = "Categorias"
		child_models = ['ItemCategoria']

	nmcategoria = models.CharField(max_length=250,verbose_name="Nome",unique=True)
	idcategoriativ = models.CharField(max_length=1,verbose_name="Situação",choices=choice_tipo_ativ,default='A')


	def __str__(self):
		return self.nmcategoria

class ItemCategoria(models.Model):
#	cdcategoria = models.OneToOneField(Categoria)
	item = models.ForeignKey(Item, verbose_name="Produto")
	def __str__(self):
		return self.item.nmproduto