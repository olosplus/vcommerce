# -*- coding: utf-8 -*-
from django.db import models
from cadastro.empresa.models import Empresa

# Create your models here.
class Unimedida(models.Model):
	class Meta:
		db_table = "unimedida"
		verbose_name = "Unidade de Medida"
		verbose_name_plural = "Unidades de Medidas"

	sgmedida = models.CharField(max_length=5,verbose_name='Abreviatura')
	nmmedida = models.CharField(max_length=100,verbose_name='Nome')
	empresa = models.ForeignKey(Empresa,verbose_name="Empresa")

	def __str__(self):
		return self.nmmedida