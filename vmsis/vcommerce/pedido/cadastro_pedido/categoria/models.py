# -*- coding: utf-8 -*-
from django.db import models

choice_tipo_ativ = (('A','Ativa'),
	('D','Inativa'))

# Create your models here.
class Categoria(models.Model):
	class Meta:
		db_table = "categoria"
		verbose_name = "Categoria"
		verbose_name_plural = "Categorias"

	nmcategoria = models.CharField(max_length=250,verbose_name="Nome",unique=True)
	idcategoriativ = models.CharField(max_length=1,verbose_name="Situação",
	    choices=choice_tipo_ativ,default='A')
	imgindex = models.IntegerField(verbose_name="Imagem")

	def __str__(self):
		return self.nmcategoria

