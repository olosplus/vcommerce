# -*- coding: utf-8 -*-
from django.db import models
from cadastro.localidade.pais.models import Pais

# Create your models here.
class Estado(models.Model):
	class Meta:
		db_table = "estado"
		verbose_name = "Estado"
		verbose_name_plural = "Estados"

	cdestado = models.CharField(max_length=2,verbose_name='Código IBGE',unique=True,db_index=True)
	sgestado = models.CharField(max_length=2,verbose_name='UF',unique=True)
	nmestado = models.CharField(max_length=40,verbose_name='Nome')
	pais = models.ForeignKey(Pais,verbose_name='País')
	dsregiao = models.CharField(max_length=20, verbose_name='Região')

	class Meta:
		ordering = ['nmestado']

	def __str__(self):
		return self.nmestado