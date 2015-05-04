# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_empresa

choice_TipoMed = (
	('C','Capacidade'),
	('V','Volume'),
	('M','Massa'))

# Create your models here.
class Unimedida(Master_empresa):
	class Meta:
		db_table = "unimedida"
		verbose_name = "Unidade de Medida"
		verbose_name_plural = "Unidades de Medidas"

	nmmedida = models.CharField(max_length=100,verbose_name='Nome')
	sgmedida = models.CharField(max_length=5,verbose_name='Abreviatura')
	qtfatorconv = models.FloatField(verbose_name="Fator de conversão")
	idtipomed = models.CharField(max_length=1, verbose_name="Tipo de Medida", choices=choice_TipoMed)

	def __str__(self):
		return self.nmmedida