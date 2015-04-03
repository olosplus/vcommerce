# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Pais(models.Model):
	"""docstring for ClassName"""
	class Meta:
		db_table = "pais"
		verbose_name = "País"
		verbose_name_plural = "Países"

	cdpais = models.CharField(max_length=10,verbose_name='Código',unique=True,db_index=True)
	sgpais = models.CharField(max_length=2,verbose_name='Sigla',unique=True,db_index=True)
	nmpais = models.CharField(max_length=250,verbose_name='Nome')

	def __str__(self):
		return self.nmpais