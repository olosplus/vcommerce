# -*- coding: utf-8 -*-
from django.db import models
from cadastro.empresa.models import Empresa

choice_marcado = (('S','Sim'),
	('N','Não'))

# Create your models here.
class Paramgeral(models.Model):
	class Meta:
		db_table = "paramgeral"
		verbose_name = "Parâmetro geral"
		verbose_name_plural = "Parâmetros gerais"

	idutilalmox = models.CharField(max_length=1,verbose_name="Utiliza almoxarifado",choices=choice_marcado)
	empresa = models.ForeignKey(Empresa,verbose_name="Empresa")