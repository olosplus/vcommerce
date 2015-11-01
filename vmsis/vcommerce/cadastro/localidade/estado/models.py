# -*- coding: utf-8 -*-
from django.db import models
from cadastro.localidade.pais.models import Pais
from vlib.control.models import Master_empresa, ControleSincronizacao

# Create your models here.
class Estado(Master_empresa, ControleSincronizacao):
	class Meta:
		db_table = "estado"
		verbose_name = "Estado"
		verbose_name_plural = "Estados"
		ordering = ['nmestado']

	cdestado = models.CharField(max_length=2,verbose_name='Código IBGE',unique=True,db_index=True)
	nmestado = models.CharField(max_length=40,verbose_name='Nome')
	sgestado = models.CharField(max_length=2,verbose_name='UF',unique=True)
	pais = models.ForeignKey(Pais,verbose_name='País')
	dsregiao = models.CharField(max_length=20, verbose_name='Região')

	def __str__(self):
		return self.nmestado