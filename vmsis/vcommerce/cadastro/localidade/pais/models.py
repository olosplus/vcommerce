# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_empresa, ControleSincronizacao

# Create your models here.
class Pais(Master_empresa, ControleSincronizacao):
	"""docstring for ClassName"""
	class Meta:
		db_table = "pais"
		verbose_name = "País"
		verbose_name_plural = "País"
		ordering = ['nmpais']

	cdpais = models.CharField(max_length=5,verbose_name='Código BACEN',unique=True,db_index=True)
	nmpais = models.CharField(max_length=250,verbose_name='País', null=False)
	cdsiscomex = models.CharField(max_length=5,verbose_name='Código SISCOMEX',db_index=True, null=True)
	sgpais2 = models.CharField(max_length=2,verbose_name='Sigla', null=True)
	sgpais3 = models.CharField(max_length=3,verbose_name='Sigla 3 letras', null=True)

	def __str__(self):
		return self.nmpais