# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Pais(models.Model):
	"""docstring for ClassName"""
	class Meta:
		db_table = "pais"
		verbose_name = "País"
		verbose_name_plural = "Países"

	cdpais = models.CharField(max_length=5,verbose_name='Código IBGE',unique=True,db_index=True)
	cdsiscomex = models.CharField(max_length=5,verbose_name='Código SISCOMEX',db_index=True, null=True)
	sgpais2 = models.CharField(max_length=2,verbose_name='Sigla',db_index=True, null=True)
	sgpais3 = models.CharField(max_length=3,verbose_name='Sigla 3 letras',db_index=True, null=True)
	nmpais = models.CharField(max_length=250,verbose_name='País', null=False)

	class Meta:
		ordering = ['nmpais']

	def __str__(self):
		return self.nmpais